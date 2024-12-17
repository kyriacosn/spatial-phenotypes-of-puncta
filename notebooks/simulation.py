import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# we setup a simple simulation of diffusing particles in a crowded cell, represented by two circles, one for the outer membrane one for the nucleus
# we use the classes Point and circle for geometrical queries like distances and intersctions



class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def add_to_plot(self,ax,color):
        ax.scatter([self.x],[self.y],color = color,s = 4)

class Circle:
    def __init__(self,x,y,radius):
        self.center = Point(x,y)
        self.radius = radius
        self.min_x = self.center.x - self.radius 
        self.min_y = self.center.y - self.radius 
        self.max_x = self.center.x + self.radius 
        self.max_y = self.center.y + self.radius 

    def signed_distance(self,x,y):
        return np.sqrt((x-self.center.x)**2 + (y-self.center.y)**2) - self.radius

    def contains(self,point):
        return self.signed_distance(point.x,point.y) < 0

    def nearest_point(self,point):
        scale = self.radius/np.sqrt((point.x-self.center.x)**2 + (point.y-self.center.y)**2) 
        return Point(self.center.x + (point.x - self.center.x) * scale,self.center.y + (point.y - self.center.y) * scale)
    
    def add_to_plot(self,ax,color):
        circle = plt.Circle((self.center.x,self.center.y), self.radius, color=color)
        ax.add_artist(circle)

    def intersects(self,other_circle):
        distance = np.sqrt((self.center.x - other_circle.center.x)**2 + (self.center.y - other_circle.center.y)**2 )
        radii_difference = np.abs(self.radius - other_circle.radius)
        radii_sum = self.radius +other_circle.radius
        return (radii_difference < distance) and (distance < radii_sum)

class Simulation:
    def __init__(self,
                 cell_radius, 
                 nucleus_radius, 
                 crowder_radius,
                 mean_density_of_crowders, 
                 production_rate,
                 degradation_rate,
                 diffusion_coefficient,
                dt):

        self.cell_radius = cell_radius
        self.nucleus_radius = nucleus_radius
        self.crowder_radius = crowder_radius
        self.mean_density_of_crowders = mean_density_of_crowders
        self.production_rate = production_rate
        self.degradation_rate = degradation_rate
        self.diffusion_coefficient = diffusion_coefficient
        self.dt =dt

        # create cell circle
        self.cell = Circle(0,0,self.cell_radius)
        
        # create nucleus
        self.nucleus = Circle(0,0,self.nucleus_radius)
        
        # generate crowders 
        number_of_crowders = np.random.poisson(self.mean_density_of_crowders*((self.cell.max_x - self.cell.min_x)*(self.cell.max_y - self.cell.min_y)))
        centers_y = np.random.uniform(self.cell.min_y,self.cell.max_y,number_of_crowders)
        centers_x = np.random.uniform(self.cell.min_x,self.cell.max_x,number_of_crowders)

        # the center of crowders needs to be inside the cell or at least the crowder intersects the cell
        self.crowders = []
        for center_x,center_y in zip(centers_x,centers_y):
            crowder = Circle(center_x,center_y,self.crowder_radius)
            if self.cell.contains(crowder.center) or self.cell.intersects(crowder):
                self.crowders.append(crowder)

        # Build KD-Tree
        self.tree = KDTree( [(crowder.center.x, crowder.center.y) for crowder in self.crowders])

        # initialize particles
        self.particles = []


    def simulate(self,n_steps):
        for i in range(n_steps):
            self.simulation_step()

    def simulation_step(self):

        n_particles_dead = np.random.binomial(len(self.particles),self.degradation_rate*self.dt)

        for i in range(n_particles_dead):
            self.particles.pop(np.random.randint(len(self.particles)))
        
        n_new_particles = np.random.poisson(self.production_rate*self.dt)

        for i in range(n_new_particles):
            angle = np.random.uniform(0,2*np.pi)
            new_particle = Point(self.nucleus.center.x + self.nucleus.radius*np.cos(angle),self.nucleus.center.y + self.nucleus.radius*np.sin(angle))                

            _, nearest_crowder_index = self.tree.query((new_particle.x,new_particle.y))

            while self.crowders[nearest_crowder_index].contains(new_particle):
                angle = np.random.uniform(0,2*np.pi)
                new_particle = Point(self.nucleus.center.x + self.nucleus.radius*np.cos(angle),self.nucleus.center.y + self.nucleus.radius*np.sin(angle))                
                _, nearest_crowder_index = self.tree.query((new_particle.x,new_particle.y))

            self.particles.append(new_particle)
            
        self.diffuse_particles()
                
    def diffuse_particles(self):
        for particle in self.particles:
            # Make a diffusion step
            particle.x += np.random.normal(0, np.sqrt(2 * self.diffusion_coefficient * self.dt))
            particle.y += np.random.normal(0, np.sqrt(2 * self.diffusion_coefficient * self.dt))

            # If it crosses a reflective boundary, reflect it of the nearest point of its surface
            if not self.cell.contains(particle):
                nearest_point = self.cell.nearest_point(particle)
                particle.x = 2*nearest_point.x - particle.x 
                particle.y = 2*nearest_point.y - particle.y

            elif self.nucleus.contains(particle):
                nearest_point = self.nucleus.nearest_point(particle)
                particle.x =  2*nearest_point.x  - particle.x 
                particle.y =  2*nearest_point.y  - particle.y 

            else:
                _, nearest_crowder_index = self.tree.query((particle.x,particle.y))
                if self.crowders[nearest_crowder_index].contains(particle):
                    nearest_point = self.crowders[nearest_crowder_index].nearest_point(particle)
                    particle.x =  2*nearest_point.x  - particle.x 
                    particle.y =  2*nearest_point.y  - particle.y 

    def plot(self, ax, plot_cell=True, plot_nucleus=True, plot_crowders=True, plot_particles=True):
        ax.set_xlim(self.cell.min_x, self.cell.max_x)
        ax.set_ylim(self.cell.min_y, self.cell.max_y)
        ax.set_aspect('equal')
    
        if plot_cell:
            self.cell.add_to_plot(ax, "black")
        if plot_crowders:
            for crowder in self.crowders:
                crowder.add_to_plot(ax, "grey")
        
        if plot_nucleus:
            self.nucleus.add_to_plot(ax, "blue")
    
        if plot_particles:
            for particle in self.particles:
                particle.add_to_plot(ax, "green")


    def get_particle_coordinates(self):
        x_coords = [particle.x for particle in self.particles]
        y_coords = [particle.y for particle in self.particles]
        return x_coords, y_coords