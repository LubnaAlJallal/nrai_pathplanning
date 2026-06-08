import os
import pickle
from code import pathfind

fifo_in = '/opt/PERCEPTION_ZedYoloTrack'
fifo_out = '/opt/PATHPLANNING_Path'

def main(args=None):
    try:
        # Make FIFO output
        os.mkfifo(fifo_out, 0o600)
        
        # FIFO input
        fd_in = os.open(fifo_in, os.O_WRONLY)
        with open(fd_in, "wb") as file:
            while True:
                cones = pickle.load(file)
                midpoints = pathfind(cones)
                
                try:
                    fd_out = os.open(fifo_out, os.O_WRONLY)
                    with open(fd_out, "wb") as fifo:
                        pickle.dump(midpoints, fifo)
                except FileNotFoundError:
                    self.get_logger().info("Could not access FIFO IN. Likely not yet configured.")
                except BrokenPipeError:
                    self.get_logger().info("FIFO OUT terminated")
                    
    except FileNotFoundError:
        self.get_logger().info("Could not access FIFO OUT. Likely not yet configured.")
    except BrokenPipeError:
        self.get_logger().info("FIFO IN terminated")

if __name__ == "__main__":
    main()
