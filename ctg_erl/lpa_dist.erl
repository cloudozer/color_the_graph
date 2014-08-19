%%
%% A distributed LPA 
%% 

-module(lpa_dist).
-export([main/3,start_node/3]).


main(File_name, Threshold, Limit) ->
	% open file and read the edges
	% spawn a new process for each node
	% send pid for each neigbor
%SN	Proc_dict = read_graph_data1(File_name),
	Proc_dict = read_graph_data(File_name),
        
	% start propagation
	% issue ticks to synchronize message exchange
	% if convergence is higher than some threshold stop
	Community_dict = run_LPA(Proc_dict,Threshold,Limit),
	
	% print communities statistics
	io:format("Communities:~n~p~n",[dict:to_list(Community_dict)]),

	io:format("Network has ~w nodes~n",
		[length(dict:fetch_keys(Proc_dict))]),
	io:format("~w communities detected in the network~n",
		[length(dict:fetch_keys(Community_dict))]).

		



% runs iterations until convergence exceeds some Threshold
run_LPA(Proc_dict,Threshold,Limit) ->
	run_LPA(0,Proc_dict,Threshold,Limit).

run_LPA(Tick,Proc_dict,Threshold,Limit) ->
	% starts next iteration of LPA
	% by broadcasting Tick message
	All_nodes = [ Val || {_,Val} <- dict:to_list(Proc_dict)],
	broadcast({tick,Tick},All_nodes),

	% then collects convergence statistics and community memberships
	% if convergence exceeds Threshold sends STOP message
	{Convergence,Label_dict} = collect_labels(Tick,dict:size(Proc_dict)),
	case Convergence >= Threshold orelse Tick > Limit of 
		false-> run_LPA(Tick+1,Proc_dict,Threshold,Limit);
		true -> 
			broadcast({quit},All_nodes),
			Label_dict
	end.


% Collects N labels from N nodes
% Returns {Convergence, Label dictionary}
collect_labels(Tick,N) ->
	collect_labels(Tick,N,N,0,dict:new()).

collect_labels(Tick,N,0,Conv,Label_dict) ->
	io:format("Iteration:~w, Convergence:~w%~n",[Tick,round(100*Conv/N)]),
	{Conv/N,Label_dict};
collect_labels(Tick,N,J,Conv,Label_dict) ->
	receive
		{label,Tick,Label,Converged} ->
			case dict:is_key(Label,Label_dict) of
				true ->	
					Label_dict1 = dict:store(Label,1+dict:fetch(Label,Label_dict),Label_dict);
				false->
					Label_dict1 = dict:store(Label,1,Label_dict)
			end
	end,
	Conv1 = Conv + Converged,
	collect_labels(Tick,N,J-1,Conv1,Label_dict1).
	
					

% broadcasts tick message to all nodes
broadcast(_,[]) ->
	ok;
broadcast(Msg,[Proc|Rest]) ->
	Proc ! Msg,
	broadcast(Msg, Rest).



read_graph_data(File_name) ->
    {ok, Device} = file:open(File_name, [read]),
    read_graph_data(Device, dict:new()).

read_graph_data(Device, Proc_dict) ->
	case io:get_line(Device, "") of
        eof  -> 
        	file:close(Device),
        	Proc_dict;
        Line -> 
% SN       	case parse_edge(Line) of
                case parse_edge1(Line) of
        		{error} ->
		        	io:format("Line: '~s'~n cannot be parsed. Edge dropped~n",[Line]),
		        	Proc_dict2 = Proc_dict;

        		{ok,{V1,V2}} ->
		        	% check if the vertices exist
		        	% spawn new processes
		        	% inform them about their neighbors
		        	case dict:is_key(V1,Proc_dict) of
		        		true -> 
		        			Pid1 = dict:fetch(V1,Proc_dict),
		        			Proc_dict1 = Proc_dict;
		        		false-> 
		        			Pid1 = spawn(lpa_dist,start_node,[self(),[],{V1,V1}]),
		        			Proc_dict1 = dict:store(V1,Pid1,Proc_dict)
		        	end,

		        	case dict:is_key(V2,Proc_dict1) of
		        		true -> 
		        			Pid2 = dict:fetch(V2,Proc_dict1),
		        			Proc_dict2 = Proc_dict1;
		        		false-> 
		        			Pid2 = spawn(lpa_dist,start_node,[self(),[],{V2,V2}]),
		        			Proc_dict2 = dict:store(V2,Pid2,Proc_dict1)
		        	end,	
		        	%io:format("~nPid1:~p\tPid2:~p~n",[Pid1,Pid2]),
		        	Pid1 ! {new_connection, Pid2},
		        	Pid2 ! {new_connection, Pid1}
		    end,
        	read_graph_data(Device,Proc_dict2) 
    end.



read_graph_data1(File_name) ->
	{ok,[Ls]} = file:consult(File_name),
	build_graph(Ls,dict:new()).

build_graph([], Proc_dict) ->
	Proc_dict;
build_graph([{Vbin1,Vbin2}|Ls], Proc_dict) ->
	V1 = binary:bin_to_list(Vbin1),
	V2 = binary:bin_to_list(Vbin2),

	case dict:is_key(V1,Proc_dict) of
		true -> 
			Pid1 = dict:fetch(V1,Proc_dict),
			Proc_dict1 = Proc_dict;
		false-> 
			Pid1 = spawn(lpa_dist,start_node,[self(),[],{V1,V1}]),
			Proc_dict1 = dict:store(V1,Pid1,Proc_dict)
	end,

	case dict:is_key(V2,Proc_dict1) of
		true -> 
			Pid2 = dict:fetch(V2,Proc_dict1),
			Proc_dict2 = Proc_dict1;
		false-> 
			Pid2 = spawn(lpa_dist,start_node,[self(),[],{V2,V2}]),
			Proc_dict2 = dict:store(V2,Pid2,Proc_dict1)
	end,	
	%io:format("~nPid1:~p\tPid2:~p~n",[Pid1,Pid2]),
	Pid1 ! {new_connection, Pid2},
	Pid2 ! {new_connection, Pid1},

	build_graph(Ls,Proc_dict2).


% 
%
start_node(Master,Neighbors,{Curr_lbl,Old_lbl}) ->
	% receives messages about:
	%	- new connections
	%	- LPA ticks
	%	- labels updates
	%	- stop LPA	
	receive
		{new_connection, Pid} ->
			Neighbors1 = lists:usort([Pid | Neighbors]),
			start_node(Master,Neighbors1,{Curr_lbl,Old_lbl});

		{tick, Tick} ->
                        broadcast({label,Tick,Curr_lbl},Neighbors),
                        case (random:uniform(100) < 65) of
                            true ->
                                New_lbl = update_label(Tick,length(Neighbors)),
                                case {New_lbl,Curr_lbl,Old_lbl} of
                                        {New_lbl,New_lbl,_} -> % converged
                                                Converged = 1,
                                                Curr1 = New_lbl,
                                                Old1 = Curr_lbl;
                                        {New_lbl,Curr_lbl,New_lbl} -> % oscilates
                                                Converged = 0.5,
                                                case length(Neighbors) > 10 of
                                                        true -> Curr1 = Curr_lbl;
                                                        false-> Curr1 = New_lbl
                                                end,
                                                %Curr1 = likely_pick_first([Curr_lbl,New_lbl],0.7),
                                                Old1 = Curr_lbl;
                                        _ ->
                                                Converged = 0,
                                                Curr1 = New_lbl,
                                                Old1 = Curr1
                                end;
                             _ ->
                                %% dont change label
                                    dont_update_label(Tick, length(Neighbors)),
                                    Converged = 0.5,
                                    Curr1 = Curr_lbl,
                                    Old1 = Old_lbl
                        end,
			Master ! {label,Tick,Curr1,Converged},
			start_node(Master,Neighbors,{Curr1,Old1});

		{quit} ->
			ok
			%io:format("~p quits~n",[self()])
	end.



randomly_pick_from(Ls) ->
	N = length(Ls),
	lists:nth(random:uniform(1,N),Ls).


likely_pick_first([First|Ls],P) ->
	case random:uniform() < P of
		true -> First;
		false-> likely_pick_first(Ls,P)
	end.


% Computes new label and returns it
update_label(Tick,N) ->
	update_label(Tick,N,[]).

update_label(_,0,Labels) ->
	Freq_labels = lists:reverse(lists:sort([{length(lists:filter(fun(X)->X==Lb end,Labels)),Lb} || 
		Lb <- lists:usort(Labels) ])),
	%io:format("Frequency of labels:~P~n",[Freq_labels,7]),
	pick_the_most_frequent(Freq_labels);
update_label(Tick,N,Labels) ->
	receive
		{label, Tick, Label} ->
			update_label(Tick,N-1,[Label|Labels])
	end.

dont_update_label(_, 0) ->
    ok;
dont_update_label(Tick, N) ->
	receive
		{label, Tick, _} ->
                    dont_update_label(Tick, N-1)	
	end.

% pick the element with largest frequency: 
% {el,freq} in the list of sorted tuples
pick_the_most_frequent([{F1,_}|_]=Ls) ->
	pick_the_most_frequent([],F1,Ls).

pick_the_most_frequent(Acc,F1,[{F1,Lb}|Rest]) ->
	pick_the_most_frequent([Lb|Acc],F1,Rest);
	
pick_the_most_frequent(Acc,_,_) ->
	%case length(Acc) >1 of
	%	true -> io:format("Tie-break: ~w candidates~n",[length(Acc)]);
	%	false-> ok
	%end,
	lists:nth(random:uniform(length(Acc)),Acc).




parse_edge(Line) ->
	Ls = string:tokens(Line,"\""),
	case length(Ls)==5 of
		true ->
			[_,V1,_,V2,_]=Ls,
			{ok,{V1,V2}};
		false->
			{error}
	end.

%SN
parse_edge1(Line) ->
        [Ls1|_] = string:tokens(Line, "\n"),
	Ls = string:tokens(Ls1,"\t"),
       %io:format("Ls = ~p~n", [Ls]),
	case length(Ls)==2 of
		true ->
			[V1,V2]=Ls,
			{ok,{V1,V2}};
		false->
			{error}
	end.
