import pygame
import numpy as np
from collections import Counter
from config import *
from physics import *
from chemistry import *
from renderer import *


def main():
    pygame.init()

    # Window and clock
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('2D Chemistry Simulator')
    clock = pygame.time.Clock()

    # Core objects
    atoms = []
    bond_manager = BondManager()
    renderer = Renderer(screen)
    molecules = Counter()

    # Drag and place state
    selected_element = None
    held_atom = None
    drag_start = None

    # Simulation state
    step_count = 0
    running = True
    paused = False

    while running:
        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if mx > sim_width_px:
                    # Click inside palette panel — select element
                    panel_x_center = sim_width_px + (width - sim_width_px) // 2
                    start_y = 80
                    spacing = 120
                    circle_radius = 25

                    for i, element in enumerate(['H', 'O', 'N', 'He']):
                        center_y = start_y + i * spacing
                        dist = np.sqrt((mx - panel_x_center)**2 + (my - center_y)**2)
                        if dist <= circle_radius:
                            selected_element = element
                            break

                elif mx < sim_width_px and selected_element is not None:
                    # Click inside sim box — spawn atom and begin drag
                    sim_pos = np.array([mx / scale, my / scale])
                    new_atom = Atom(selected_element, sim_pos)
                    atoms.append(new_atom)
                    held_atom = new_atom
                    drag_start = (mx, my)

            elif event.type == pygame.MOUSEMOTION:
                if held_atom is not None:
                    # Update held atom position to follow cursor
                    mx, my = event.pos
                    held_atom.pos[0] = mx / scale
                    held_atom.pos[1] = my / scale

            elif event.type == pygame.MOUSEBUTTONUP:
                if held_atom is not None and drag_start is not None:
                    # Release atom — assign velocity from drag vector
                    mx, my = event.pos
                    dx = mx - drag_start[0]
                    dy = my - drag_start[1]
                    held_atom.vel[0] = dx * velocity_scale
                    held_atom.vel[1] = dy * velocity_scale
                    held_atom.held = False
                    held_atom = None
                    drag_start = None

        if not paused:
            # Physics step
            velocity_verlet(atoms, bond_manager, dt)
            step_count += 1

            # Bond check every N steps
            if step_count % bond_check_interval == 0:
                bond_manager.update_bonds(atoms)

            # Molecule detection every N steps
            if step_count % molecule_check_interval == 0:
                molecules = detect_molecules(atoms)

        renderer.draw(atoms, bond_manager, molecules, selected_element)

    pygame.quit()


if __name__ == '__main__':
    main()
