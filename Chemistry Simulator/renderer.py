import pygame
import numpy as np
from config import *
from chemistry import *
from physics import *


def sim_to_screen(pos):
    # Convert sim coordinates to screen pixel coordinates
    return (int(pos[0] * scale), int(pos[1] * scale))


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.large_font = pygame.font.SysFont('consolas', 24)
        self.small_font = pygame.font.SysFont('consolas', 18)

    def draw_background(self):
        # Sim box
        pygame.draw.rect(self.screen, simulation_background_color, (0, 0, sim_width_px, height))
        # Element palette panel
        pygame.draw.rect(self.screen, panel_background_color, (sim_width_px, 0, width - sim_width_px, height))

    def draw_bonds(self, atoms, bond_manager):
        # Quick atom lookup by id
        atom_lookup = {atom.id: atom for atom in atoms}

        for pair in bond_manager.bonds:
            id_i, id_j = tuple(pair)
            atom_i = atom_lookup[id_i]
            atom_j = atom_lookup[id_j]

            # Screen positions as numpy arrays for offset math
            screen_i = np.array(sim_to_screen(atom_i.pos))
            screen_j = np.array(sim_to_screen(atom_j.pos))

            # Bond order — default single if not specified
            element_pair = frozenset({atom_i.element, atom_j.element})
            order = bond_orders.get(element_pair, 1)

            # Average color of the two atoms
            color_i = elements[atom_i.element]['color']
            color_j = elements[atom_j.element]['color']
            avg_color = tuple((np.array(color_i) + np.array(color_j)) // 2)

            # Perpendicular unit vector for multi-line bonds
            bond_vec = screen_j - screen_i
            bond_len = np.linalg.norm(bond_vec)
            perp = np.array([-bond_vec[1], bond_vec[0]]) / bond_len if bond_len > 0 else np.array([0, 1])
            offset = perp * 3

            if order == 1:
                # Single bond
                pygame.draw.line(self.screen, avg_color,
                                 tuple(screen_i.astype(int)),
                                 tuple(screen_j.astype(int)), 2)
            elif order == 2:
                # Double bond — two parallel lines
                pygame.draw.line(self.screen, avg_color,
                                 tuple((screen_i + offset).astype(int)),
                                 tuple((screen_j + offset).astype(int)), 2)
                pygame.draw.line(self.screen, avg_color,
                                 tuple((screen_i - offset).astype(int)),
                                 tuple((screen_j - offset).astype(int)), 2)
            elif order == 3:
                # Triple bond — center line plus two offset lines
                pygame.draw.line(self.screen, avg_color,
                                 tuple(screen_i.astype(int)),
                                 tuple(screen_j.astype(int)), 2)
                pygame.draw.line(self.screen, avg_color,
                                 tuple((screen_i + offset).astype(int)),
                                 tuple((screen_j + offset).astype(int)), 2)
                pygame.draw.line(self.screen, avg_color,
                                 tuple((screen_i - offset).astype(int)),
                                 tuple((screen_j - offset).astype(int)), 2)

    def draw_atoms(self, atoms):
        for atom in atoms:
            screen_pos = sim_to_screen(atom.pos)
            color = elements[atom.element]['color']
            radius = elements[atom.element]['radius_pixel']

            if atom.held:
                # Semi-transparent ghost while dragging
                ghost_surface = pygame.Surface((radius * 2 + 6, radius * 2 + 6), pygame.SRCALPHA)
                pygame.draw.circle(ghost_surface, (*color, 128), (radius + 3, radius + 3), radius)
                self.screen.blit(ghost_surface, (screen_pos[0] - radius - 3, screen_pos[1] - radius - 3))
            else:
                # Filled circle, white outline, element label
                pygame.draw.circle(self.screen, color, screen_pos, radius)
                pygame.draw.circle(self.screen, (255, 255, 255), screen_pos, radius, 1)
                text_surface = self.small_font.render(atom.element, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=screen_pos)
                self.screen.blit(text_surface, text_rect)

    def draw_flash_effects(self, bond_manager):
        for i in range(len(bond_manager.flash_events)):
            pos, age = bond_manager.flash_events[i]
            screen_pos = sim_to_screen(pos)

            # Expanding radius and fading alpha over 10 frames
            radius = int(age * 3)
            alpha = int(255 * (1 - age / 10))

            if radius > 0:
                size = radius * 2 + 4
                flash_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(flash_surface, (255, 255, 255, alpha),
                                   (size // 2, size // 2), radius, 2)
                self.screen.blit(flash_surface,
                                 (screen_pos[0] - size // 2, screen_pos[1] - size // 2))

            bond_manager.flash_events[i] = (pos, age + 1)

        # Remove expired events
        bond_manager.flash_events = [
            (pos, age) for (pos, age) in bond_manager.flash_events if age < 10
        ]

    def draw_panel(self, selected_element):
        panel_x_center = sim_width_px + (width - sim_width_px) // 2
        start_y = 80
        spacing = 120
        circle_radius = 25

        # Panel title
        title = self.large_font.render('Elements', True, (200, 200, 200))
        self.screen.blit(title, title.get_rect(center=(panel_x_center, 30)))

        for i, element in enumerate(['H', 'O', 'N', 'He']):
            center_y = start_y + i * spacing
            color = elements[element]['color']

            # Element circle
            pygame.draw.circle(self.screen, color, (panel_x_center, center_y), circle_radius)

            # Selection ring
            if element == selected_element:
                pygame.draw.circle(self.screen, (255, 255, 255),
                                   (panel_x_center, center_y), circle_radius + 3, 2)

            # Element label below circle
            label = self.small_font.render(element, True, (255, 255, 255))
            self.screen.blit(label, label.get_rect(center=(panel_x_center, center_y + circle_radius + 12)))

    def draw_hud(self, molecule_counts):
        # Molecule counter title
        title = self.large_font.render('Molecules', True, (200, 200, 200))
        self.screen.blit(title, (10, 10))

        y_offset = 35
        for name, count in molecule_counts.items():
            if name == 'unknown':
                continue
            line = self.small_font.render(f"{name}: {count}", True, (200, 200, 200))
            self.screen.blit(line, (10, y_offset))
            y_offset += 22

    def draw(self, atoms, bond_manager, molecule_counts, selected_element):
        self.draw_background()
        self.draw_bonds(atoms, bond_manager)
        self.draw_flash_effects(bond_manager)
        self.draw_atoms(atoms)
        self.draw_panel(selected_element)
        self.draw_hud(molecule_counts)
        pygame.display.flip()
