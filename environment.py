#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import matplotlib.pyplot as plt #Library for constructing plots
import io #Input, output operation library for reading, opening file objects
import matplotlib.animation as animation #Library for displaying animation
from PIL import Image
import matplotlib.image as mpimg #Library for reading files
import datetime #Library for getting timestamp
class Environment:
    def __init__(self,water=None):
        
        if water is None:
            water = {7}  # set default taps with water
        self.water = water
        
        self.running_tap = mpimg.imread('runningTap.png')
        self.closed_tap = mpimg.imread('closedTap.png')
        self.human = mpimg.imread('human.png')
        
        self.graph = {
            1: [2, 6],
            2: [1, 3, 7],
            3: [2, 4, 8],
            4: [3, 5, 9],
            5: [4, 10],
            6: [1, 7, 11],
            7: [2, 6, 8, 12],
            8: [3, 7, 9, 13],
            9: [4, 8, 10, 14],
            10: [5, 9, 15],
            11: [6, 12, 16],
            12: [7, 11, 13, 17],
            13: [8, 12, 14, 18],
            14: [9, 13, 15, 19],
            15: [10, 14, 20],
            16: [11, 17, 21],
            17: [12, 16, 18, 22],
            18: [13, 17, 19, 23],
            19: [14, 18, 20, 24],
            20: [15, 19, 25],
            21: [16, 22],
            22: [17, 21, 23],
            23: [18, 22, 24],
            24: [19, 23, 25],
            25: [20, 24]
        }

        self.field = {
            1: (0, 8),
            2: (2, 8),
            3: (4, 8),
            4: (6, 8),
            5: (8, 8),
            6: (0, 6),
            7: (2, 6),
            8: (4, 6),
            9: (6, 6),
            10: (8, 6),
            11: (0, 4),
            12: (2, 4),
            13: (4, 4),
            14: (6, 4),
            15: (8, 4),
            16: (0, 2),
            17: (2, 2),
            18: (4, 2),
            19: (6, 2),
            20: (8, 2),
            21: (0, 0),
            22: (2, 0),
            23: (4, 0),
            24: (6, 0),
            25: (8, 0)
        }

        self.taps_with_water = self.water
        self.taps_without_water = set(self.field.keys()) - self.taps_with_water
        self.scale_factor = 2

    def scaled_extent(self, coord):
        x, y = self.field[coord]
        return [x - 0.5 * self.scale_factor, x + 0.5 * self.scale_factor, y - 0.5 * self.scale_factor, y + 0.5 * self.scale_factor]
    
    #Display animation based on parameters obtained from the BFS or DFS agent
    def display_animation(self,time_taken,node_count,max_depth,peak_memory,all_movements):
        print(f"Time taken: {time_taken:.2f} milliseconds")
        print(f"Number of nodes visited: {node_count}")
        print(f"Number of paths taken: {node_count - 1 if node_count > 0 else 0}")
        print(f"Maximum depth reached: {max_depth}")
        print(f"Peak memory usage: {peak_memory / 1024:.2f} KB")
            
        print("Loading Visuals...")
        
        fig, ax = plt.subplots(figsize=(10, 10)) #defining a graph figure
        ax.axis('off') #Remove labels on axis
        ax.set_aspect('equal') #Make sure units are equal
        ax.set_xlim(-2, 10) #limit of the stretch on the x axis
        ax.set_ylim(-2, 10) #limit of the stretch on the y axis
        
        # Load and display background image
        background_img = mpimg.imread('field.jpeg')
        ax.imshow(background_img, extent=[-2, 10, -2, 10], aspect='auto')
        
        # Load and display a rock, unaccessible path at node 5
#         rock_img = mpimg.imread('rock.png')  # Load rock image
#         rock_x, rock_y = self.field[12]  # Get coordinates for node 5
#         ax.imshow(rock_img, extent=[rock_x-0.5, rock_x+0.5, rock_y-0.5, rock_y+0.5])
        
        #Display all taps with water in figure
        for tap in self.taps_with_water:
            x, y = self.field[tap]
            ax.imshow(self.running_tap, extent=[x-0.5, x+0.5, y-0.5, y+0.15])
            
        #Display all taps without water in figure
        for tap in self.taps_without_water:
            x, y = self.field[tap]
            ax.imshow(self.closed_tap, extent=[x-0.5, x+0.5, y-0.5, y+0.5])
        
        #Increase the size of the agent and display
        self.agent = agent_image = ax.imshow(self.human, extent=self.scaled_extent(1))
        
        #Function to display the positions of the agent at every nodes
        def update(num):
            if num < len(all_movements):
                agent_extent = self.scaled_extent(all_movements[num])
                agent_image.set_extent(agent_extent)
            return agent_image,
        
        #Display animation
        self.ani = animation.FuncAnimation(fig, update, frames=len(all_movements), interval=1000, repeat=False)
        
        plt.show()
    
    '''
    To save the animation for external observation we use Pillow.
    We start by creating a frame array and storing all movements in the array.
    This helps to insert the agents movement into the file that will be created
    '''
    def save_animation(self,movements,prefix):
        frames = []
        all_movements = movements
        if not all_movements:
            print("Nothing to be saved")
            return
        #function to store frames
        print("Saving file...")
        def capture_frame(num):
            if num < len(all_movements):
                agent_extent = self.scaled_extent(all_movements[num])
                self.agent.set_extent(agent_extent)
                plt.draw()

                # create buffer and store each set of bytes
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                buf.seek(0)
                img = Image.open(buf).copy()  # Load and copy the image data
                frames.append(img)
                buf.close()

        for i in range(len(all_movements)):
            capture_frame(i)
            
        #We attach current time to file names so as to be able to track savings
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f'{prefix}._{current_time}.gif'

        # Save the frames as a GIF using Pillow
        frames[0].save(filename, save_all=True, append_images=frames[1:], loop=1, duration=1000)
        print(f"File saved as {filename}")

