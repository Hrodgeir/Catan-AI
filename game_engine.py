import random

class GameEngine:
    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    #TODO: actually test this method
    def give_resources_by_dice_roll(self, board, players, dice_val):
        rewarded_tiles = board.tile_by_dice_val[str(dice_val)]

        for vertex in board.vertices:
            for tile in rewarded_tiles:
                if vertex.tile_id == tile:
                    resource = players[str(vertex.owner)].resources[tile_type] #hope it actually caches the reference
                    resource = resource + 1

    def positioning_turns(self, players, total_turns=2):
        turn_counter = 0

        while(turn_counter < total_turns):
            for player in players:
                print("Player " + str(player.id))
                #do stuff

            for player in reversed(players):
                #do stuff again
                print("Player " + str(player.id))
            turn_counter = turn_counter + 2


        


            
            
        
            



        
    
        
