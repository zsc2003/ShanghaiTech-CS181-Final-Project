def reinforcement_learning():
    # TODO
    pass





alpha = 0.5
discount_factor = 0.99
depth = 2

def train_qlearning():
    qvalue_grid = {}


    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@train
    epochs =??
    epsilon = 0.3
    i = 0
    count_win = 0
    four_step_before = None
    #训练的时候跑很多个game
    while(i < epochs):
        i += 1
        if(i % 50 == 0):
            # print(list(qvalue_grid.values()))
            print(i)
        
        game = Game(win,WHITE)
        is_run = True
        count_step = 0
        while is_run:
            if game.turn == ai_turn:
                score,new_board = minimax([0],game.board, ai_turn, depth, game)  
                # raise RuntimeError(new_board)
                # print(4)        
                if new_board:
                    game.ai_move(new_board)
                if(new_board == None):
                    if game.board.winner() != None:
                        game.draw_winner()
                        is_run = False
                    continue
                #AI用minimax决策
                # pygame.time.delay(100)
            else:
                # if(count_step % 4 = )
                count_step += 1
                if(count_step > 150):
                    break
                #这里就是有个问题就是，会出现白棋和黑棋的王自己就在自己的地方来回走，游戏一直不结束
                # if(game.board == four_step_before):
                #     is_run = False
                #     continue
                # if(count_step % 10 == 0):
                #     four_step_before = game.board
                valid_moves = get_all_moves([0],game.board,WHITE,game)
                # raise RuntimeError(valid_moves)
                max_action = None
                max_q_value = -9999
                for num_board in range(len(valid_moves)):
                    new_board = valid_moves[num_board]
                    #因为这里的action是确定的，不是选了会有不同概率的效果的， 所以我直接用前后的board来代表qstate，碰到了就初始化为0
                    if((game.board, new_board) not in qvalue_grid.keys()):
                        qvalue_grid[(game.board, new_board)] = 0

                    max_for_next_step = 0   #这里是处理Q（S‘）取max
                    valid_moves_1 = get_all_moves([0],new_board,WHITE,game)
                    for num_board_1 in range(len(valid_moves_1)):
                        new_board_1 = valid_moves_1[num_board_1]
                        if((new_board, new_board_1) not in qvalue_grid.keys()):
                            qvalue_grid[(new_board, new_board_1)] = 0
                        if(qvalue_grid[(new_board, new_board_1)] > max_for_next_step):
                            max_for_next_step = qvalue_grid[(new_board, new_board_1)]
                    #更新Q-value   这里用的evaluatedist， 然后reward 加了一个负号他的qvalue训出来会是正的，可能是什么地方取反了我没看到
                    qvalue_grid[(game.board, new_board)] = (1 - alpha) * qvalue_grid[(game.board, new_board)] + alpha * (-(new_board.evaluate_dist(WHITE) - game.board.evaluate_dist(WHITE)) + discount_factor * max_for_next_step)
                    #选出max 的Q（S）
                    if(qvalue_grid[(game.board, new_board)] > max_q_value):
                        max_q_value = qvalue_grid[(game.board, new_board)]
                        max_action = new_board

                #另外一个情况  （好像）    是，会出现只剩一个子，但是子在最边上而且唯一能走的被堵了，没有能走的地方了。
                if(len(valid_moves) == 0):
                    if game.board.winner() != None:
                        game.draw_winner()
                        is_run = False
                    continue

                #这里是加了一些随机的探索， except用不到
                flip_coin = random.random()
                if(flip_coin > epsilon):
                    try:
                        
                        game.ai_move(max_action)

                    except:
                        pygame.time.delay(5000)
                else:
                    try:
                        game.ai_move(random.choice(valid_moves))
                    except:
                        # raise RuntimeError(valid_moves)
                        pygame.time.delay(5000)
                # epsilon *= 0.99


                # get_all_moves


                # game.change_turn()

                #判断是否有人获胜
            if game.board.winner() != None:
                # game.draw_winner()
                if(game.board.winner() == WHITE):
                    # count_win += 1
                    print(count_win)
                is_run = False
                
            
            game.update()
        epsilon *= 0.99

    # with open("D:/CS181/project/draughtAI-main/draughtAI-main/ckpts.pkl",'wb')as f:
    #     pickle.dump(qvalue_grid,f)
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@train
    # print("load_begin")
    # with open("D:/CS181/project/draughtAI-main/draughtAI-main/ckpts.pkl", 'rb')as f1:
    #     qvalue_grid = pickle.load(f1)
    # print("load_finish")
    # qvalue_grid
        
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@test
    
    epochs_1 = 100
    epsilon = 0.3
    i = 0
    count_win = 0
    four_step_before = None
    depth_1 = 2
    #我之前好像用depth2训练的同时看能不能赢好像不行，试了一下用depth3训练在depth2测试好像也不太行，所以就怀疑我代码有点问题
    while(i < epochs_1):
        i += 1
        # if(i % 50 == 0):
        #     print(i)
        # print(i)
        
        game = Game(win,WHITE)
        is_run = True
        count_step = 0
        count_1 = 0
        while is_run:
            count_1 +=1

            #陷入死循环时跳出
            if(count_1 > 150):
                break
            if game.turn == ai_turn:
                # score,new_board = minimax([0],game.board, ai_turn, depth_1, game)  
                valid_moves = get_all_moves([0],game.board,ai_turn,game)
                if(len(valid_moves) == 0):
                    if game.board.winner() != None:
                        game.draw_winner()
                        is_run = False
                    continue
                new_board = random.choice(valid_moves)
                #随机agent
                # raise RuntimeError(new_board)
                # print(4)        
                if new_board:
                    game.ai_move(new_board)

                # pygame.time.delay(100)
            else:
                # if(count_step % 4 = )
                count_step += 1
                if(count_step > 150):
                    break
                # if(game.board == four_step_before):
                #     is_run = False
                #     continue
                # if(count_step % 10 == 0):
                #     four_step_before = game.board
                valid_moves = get_all_moves([0],game.board,WHITE,game)
                # raise RuntimeError(valid_moves)
                if(len(valid_moves) == 0):
                    if game.board.winner() != None:
                        game.draw_winner()
                        is_run = False
                    continue

                #直接用最大的qvalue
                max_action = valid_moves[0]
                max_q_value = -9999
                for num_board in range(len(valid_moves)):
                    try:
                        new_board = valid_moves[num_board]
                    
                
                        if(qvalue_grid[(game.board, new_board)] > max_q_value):
                            # max_q_value = qvalue_grid[(game.board, new_board)]
                            max_action = new_board
                    except:
                        #这里是因为可能出现训练时没出现过的state， 相当于qvalue是0直接跳过就行
                        continue


                if(len(valid_moves) == 0):
                    if game.board.winner() != None:
                        game.draw_winner()
                        is_run = False
                    continue
                flip_coin = random.random()
                if(flip_coin > epsilon):
                    try:
                        
                        game.ai_move(max_action)

                    except:
                        pygame.time.delay(100)
                else:
                    try:
                        game.ai_move(random.choice(valid_moves))
                    except:
                        # raise RuntimeError(valid_moves)
                        pygame.time.delay(100)
                # epsilon *= 0.99


                # get_all_moves


                # game.change_turn()

                #判断是否有人获胜
            if game.board.winner() != None:
                # game.draw_winner()
                if(game.board.winner() == WHITE):
                    count_win += 1
                    print(count_win)
                is_run = False
                
            
            game.update()
        # epsilon *= 0.99
    print(count_win)
        

