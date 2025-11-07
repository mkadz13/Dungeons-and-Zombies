import pygame
import random
import math

# Initialize pygame
pygame.init()

# Game Constants - Windowed mode
WIDTH, HEIGHT = 1200, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GOLD = (255, 215, 0)
PLAYER_SPEED = 5
ZOMBIE_SPEED = 2
TILE_SIZE = 40

# Initialize Screen - Windowed mode
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeons & Zombies - Enhanced Edition")
clock = pygame.time.Clock()

# Load Assets
wall_img = pygame.image.load('images/Dungeon Side Wall.png').convert_alpha()
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

small_wall_img = pygame.image.load('images/small wall.jpg').convert()
small_wall_img = pygame.transform.scale(small_wall_img, (TILE_SIZE, TILE_SIZE))

zombie_img = pygame.image.load('images/zombie.png').convert_alpha()
zombie_img = pygame.transform.scale(zombie_img, (40, 40))

player_img = pygame.image.load('images/luffy1.png').convert()
player_img = pygame.transform.scale(player_img, (40, 40))

ghost_img = pygame.image.load('images/ghost.png').convert_alpha()
ghost_img = pygame.transform.scale(ghost_img, (40, 40))

def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Level Generation System
def generate_level_layout(level_num):
    """Generate different layouts for each level with increasing difficulty"""
    width, height = 30, 20  # Grid size
    map_data = [[0 for _ in range(width)] for _ in range(height)]
    
    # Add borders
    for i in range(width):
        map_data[0][i] = 1
        map_data[height-1][i] = 1
    for i in range(height):
        map_data[i][0] = 1
        map_data[i][width-1] = 1
    
    if level_num == 1:
        # Level 1: Simple layout with few obstacles
        return generate_simple_layout(map_data, width, height)
    elif level_num == 2:
        # Level 2: Cross pattern
        return generate_cross_layout(map_data, width, height)
    elif level_num == 3:
        # Level 3: Maze-like
        return generate_maze_layout(map_data, width, height)
    elif level_num == 4:
        # Level 4: Complex maze
        return generate_complex_maze(map_data, width, height)
    else:
        # Level 5+: Procedural generation
        return generate_procedural_layout(map_data, width, height, level_num)

def generate_simple_layout(map_data, width, height):
    """Level 1: Simple layout with few obstacles"""
    # Create a simple, clean layout
    # Corner obstacles
    for i in range(3, 6):
        map_data[3][i] = 2  # Top left
        map_data[height-4][i] = 2  # Bottom left
    for i in range(width-6, width-3):
        map_data[3][i] = 2  # Top right
        map_data[height-4][i] = 2  # Bottom right
    
    # Center obstacles
    obstacles = [(8, 6), (15, 8), (22, 12), (10, 14)]
    for x, y in obstacles:
        if 0 < x < width-1 and 0 < y < height-1:
            map_data[y][x] = 2
    return map_data

def generate_cross_layout(map_data, width, height):
    """Level 2: Cross pattern with gaps"""
    # Horizontal line with strategic gaps
    for i in range(6, 24):
        if i not in [10, 11, 12, 13, 14, 15]:  # Leave gaps for movement
            map_data[height//2][i] = 2
    
    # Vertical line with gaps
    for i in range(4, 16):
        if i not in [8, 9, 10, 11]:  # Leave gaps for movement
            map_data[i][width//2] = 2
    
    # Corner barriers
    for i in range(2, 5):
        map_data[2][i] = 2
        map_data[height-3][i] = 2
        map_data[2][width-1-i] = 2
        map_data[height-3][width-1-i] = 2
    return map_data

def generate_maze_layout(map_data, width, height):
    """Level 3: Structured maze with clear paths"""
    # Create a proper maze with clear corridors
    # Horizontal walls with gaps
    for i in range(2, width-2, 4):
        for j in range(3, height-3):
            if j % 4 != 0:  # Leave gaps every 4th row
                map_data[j][i] = 2
    
    # Vertical walls with gaps
    for j in range(2, height-2, 4):
        for i in range(3, width-3):
            if i % 4 != 0:  # Leave gaps every 4th column
                map_data[j][i] = 2
    
    # Strategic pillars
    pillars = [(6, 6), (12, 10), (18, 8), (24, 12)]
    for x, y in pillars:
        if 0 < x < width-1 and 0 < y < height-1:
            map_data[y][x] = 2
    return map_data

def generate_complex_maze(map_data, width, height):
    """Level 4: Complex but navigable maze"""
    # Outer ring of obstacles
    for i in range(3, width-3):
        if i % 3 == 0:
            map_data[3][i] = 2
            map_data[height-4][i] = 2
    
    for j in range(3, height-3):
        if j % 3 == 0:
            map_data[j][3] = 2
            map_data[j][width-4] = 2
    
    # Inner structured obstacles
    for i in range(6, width-6, 3):
        for j in range(6, height-6, 3):
            if (i + j) % 6 == 0:  # Deterministic pattern
                map_data[j][i] = 2
                if i+1 < width-1:
                    map_data[j][i+1] = 2
                if j+1 < height-1:
                    map_data[j+1][i] = 2
    
    # Ensure main paths are clear
    for i in range(8, width-8, 6):
        for j in range(8, height-8, 6):
            map_data[j][i] = 0
            map_data[j][i+1] = 0
            map_data[j+1][i] = 0
    return map_data

def generate_procedural_layout(map_data, width, height, level_num):
    """Level 5+: Deterministic complex layouts"""
    # Use deterministic patterns based on level number
    # Level 5: Spiral pattern
    if level_num == 5:
        # Create spiral obstacles
        for i in range(4, width-4, 2):
            for j in range(4, height-4, 2):
                if (i + j) % 4 == 0:
                    map_data[j][i] = 2
                    if i+1 < width-1:
                        map_data[j][i+1] = 2
                    if j+1 < height-1:
                        map_data[j+1][i] = 2
    
    # Level 6: Diamond pattern
    elif level_num == 6:
        center_x, center_y = width // 2, height // 2
        for i in range(2, width-2):
            for j in range(2, height-2):
                if abs(i - center_x) + abs(j - center_y) < 8:
                    if (i + j) % 3 == 0:
                        map_data[j][i] = 2
    
    # Level 7: Grid pattern
    elif level_num == 7:
        for i in range(3, width-3, 3):
            for j in range(3, height-3, 3):
                if (i + j) % 6 == 0:
                    map_data[j][i] = 2
                    if i+1 < width-1:
                        map_data[j][i+1] = 2
                    if j+1 < height-1:
                        map_data[j+1][i] = 2
                        map_data[j+1][i+1] = 2
    
    # Level 8+: Complex deterministic patterns
    else:
        # Create complex but navigable patterns
        for i in range(2, width-2, 2):
            for j in range(2, height-2, 2):
                if (i * j) % (level_num + 3) == 0:
                    map_data[j][i] = 2
                    if i+1 < width-1:
                        map_data[j][i+1] = 2
                    if j+1 < height-1:
                        map_data[j+1][i] = 2
    
    # Ensure main paths are always clear
    for i in range(4, width-4, 4):
        for j in range(4, height-4, 4):
            map_data[j][i] = 0
            if i+1 < width-1:
                map_data[j][i+1] = 0
            if j+1 < height-1:
                map_data[j+1][i] = 0
                map_data[j+1][i+1] = 0
    
    return map_data

# Generate initial level
current_level_map = generate_level_layout(1)

# Wall Class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_img
        self.rect = self.image.get_rect(topleft=(x, y))

# SmallWall Class
class SmallWall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = small_wall_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x + (TILE_SIZE - self.rect.width) // 2, y + (TILE_SIZE - self.rect.height) // 2)

# Enhanced Player Class with screen boundaries
class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.health = 100
        self.max_health = 100
        self.speed_boost = 0
        self.damage_boost = 1
        self.shield_active = False
        self.invulnerable = False
        self.invulnerability_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -(PLAYER_SPEED + self.speed_boost)
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED + self.speed_boost
        if keys[pygame.K_UP]:
            dy = -(PLAYER_SPEED + self.speed_boost)
        if keys[pygame.K_DOWN]:
            dy = PLAYER_SPEED + self.speed_boost

        # Move horizontally and check collisions
        self.rect.x += dx
        if (pygame.sprite.spritecollide(self, walls, False) or
            pygame.sprite.spritecollide(self, small_walls, False) or
            self.rect.left < 0 or self.rect.right > WIDTH):
            self.rect.x -= dx

        # Move vertically and check collisions
        self.rect.y += dy
        if (pygame.sprite.spritecollide(self, walls, False) or
            pygame.sprite.spritecollide(self, small_walls, False) or
            self.rect.top < 0 or self.rect.bottom > HEIGHT):
            self.rect.y -= dy
        
        # Update invulnerability
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time >= self.invulnerability_timer:
                self.invulnerable = False

    def take_damage(self, damage):
        if not self.invulnerable and not self.shield_active:
            self.health -= damage
            if self.health <= 0:
                return True  # Player died
            else:
                # Make player temporarily invulnerable
                self.invulnerable = True
                self.invulnerability_timer = pygame.time.get_ticks() + 1000  # 1 second
        return False

# Enhanced Zombie Class with AI
class Zombie(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = zombie_img
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.health = 50
        self.damage = 15
        self.attack_cooldown = 0
        self.last_attack_time = 0

    def update(self):
        # Calculate direction to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Move towards player
            self.rect.x += dx * ZOMBIE_SPEED
            self.rect.y += dy * ZOMBIE_SPEED
            
            # Check wall collisions
            if (pygame.sprite.spritecollide(self, walls, False) or
                pygame.sprite.spritecollide(self, small_walls, False)):
                self.rect.x -= dx * ZOMBIE_SPEED
                self.rect.y -= dy * ZOMBIE_SPEED

    def can_attack(self, player):
        current_time = pygame.time.get_ticks()
        distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + 
                           (player.rect.centery - self.rect.centery)**2)
        
        if distance < 50 and current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            return True
        return False

# Ghost Class with phase ability
class Ghost(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = ghost_img
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.health = 30
        self.damage = 10
        self.speed = 3
        self.attack_cooldown = 0
        self.last_attack_time = 0
        self.can_phase = True

    def update(self):
        # Calculate direction to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Move towards player
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            
            # Ghosts can phase through small walls but not main walls
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x -= dx * self.speed
                self.rect.y -= dy * self.speed

    def can_attack(self, player):
        current_time = pygame.time.get_ticks()
        distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + 
                           (player.rect.centery - self.rect.centery)**2)
        
        if distance < 50 and current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            return True
        return False

# Gold Bar Class
class Gold(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect(center=(x, y))
        self.value = 1
        self.animation_frame = 0
        self.animation_speed = 0.15
        
    def update(self):
        # Spinning animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2 * math.pi:
            self.animation_frame = 0
        
        # Rotate coin
        angle = math.degrees(self.animation_frame)
        self.image = pygame.transform.rotate(pygame.Surface((20, 20)), angle)
        self.image.fill(GOLD)

# Power-up Class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type="health"):
        super().__init__()
        self.powerup_type = powerup_type
        self.value = 0
        self.duration = 0
        self.animation_frame = 0
        self.animation_speed = 0.1
        
        # Create visual representation
        if powerup_type == "health":
            self.image = pygame.Surface((25, 25))
            self.image.fill((255, 0, 0))
            self.value = 25
        elif powerup_type == "speed":
            self.image = pygame.Surface((25, 25))
            self.image.fill((0, 255, 0))
            self.value = 2
            self.duration = 10000  # 10 seconds
        elif powerup_type == "damage":
            self.image = pygame.Surface((25, 25))
            self.image.fill((255, 255, 0))
            self.value = 1.5
            self.duration = 15000  # 15 seconds
        elif powerup_type == "shield":
            self.image = pygame.Surface((25, 25))
            self.image.fill((0, 0, 255))
            self.value = 1
            self.duration = 20000  # 20 seconds
        
        self.rect = self.image.get_rect(center=(x, y))
        self.original_image = self.image.copy()
        
    def update(self):
        # Animate powerup
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2 * math.pi:
            self.animation_frame = 0
        
        # Floating animation
        offset = math.sin(self.animation_frame) * 3
        self.rect.y += offset
        
        # Pulsing effect
        scale = 1 + math.sin(self.animation_frame * 2) * 0.1
        new_size = int(25 * scale)
        self.image = pygame.transform.scale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)

# Game State Management
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"

class GameManager:
    def __init__(self):
        self.current_state = GameState.PLAYING
        self.current_level = 1
        self.score = 0
        self.coins_collected = 0
        self.required_coins = 3
        self.lives = 3

def spawn_new_level():
    """Spawn new level with more enemies and coins"""
    global all_sprites, zombies, ghosts, gold_bars, powerups, walls, small_walls, current_level_map, player
    
    # Clear existing entities
    zombies.empty()
    ghosts.empty()
    gold_bars.empty()
    powerups.empty()
    walls.empty()
    small_walls.empty()
    
    # Remove entities from all_sprites
    for sprite in list(all_sprites):
        if sprite != player:
            all_sprites.remove(sprite)
    
    # Generate new level layout
    current_level_map = generate_level_layout(game_manager.current_level)
    
    # Create walls from the new layout
    for row_index, row in enumerate(current_level_map):
        for col_index, tile in enumerate(row):
            x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
            if tile == 1:  # Main walls
                wall = Wall(x, y)
                all_sprites.add(wall)
                walls.add(wall)
            elif tile == 2:  # Small walls/obstacles
                small_wall = SmallWall(x, y)
                all_sprites.add(small_wall)
                small_walls.add(small_wall)
    
    # Move player to valid position
    player_x, player_y = find_valid_spawn_position()
    player.rect.centerx = player_x
    player.rect.centery = player_y
    
    # Spawn more enemies based on level
    enemy_count = 2 + game_manager.current_level
    for i in range(enemy_count):
        # Find valid spawn position (not on walls)
        attempts = 0
        while attempts < 100:
            x = random.randint(100, WIDTH-100)
            y = random.randint(100, HEIGHT-100)
            # Check if position is clear
            if not any(wall.rect.collidepoint(x, y) for wall in walls) and \
               not any(swall.rect.collidepoint(x, y) for swall in small_walls):
                if i % 2 == 0:  # Spawn zombies
                    zombie = Zombie(x, y)
                    all_sprites.add(zombie)
                    zombies.add(zombie)
                else:  # Spawn ghosts
                    ghost = Ghost(x, y)
                    all_sprites.add(ghost)
                    ghosts.add(ghost)
                break
            attempts += 1
    
    # Spawn coins
    coin_count = game_manager.required_coins
    for i in range(coin_count):
        # Find valid spawn position
        attempts = 0
        while attempts < 100:
            x = random.randint(100, WIDTH-100)
            y = random.randint(100, HEIGHT-100)
            # Check if position is clear
            if not any(wall.rect.collidepoint(x, y) for wall in walls) and \
               not any(swall.rect.collidepoint(x, y) for swall in small_walls):
                gold = Gold(x, y)
                all_sprites.add(gold)
                gold_bars.add(gold)
                break
            attempts += 1
    
    # Spawn power-up (random chance)
    if random.random() < 0.5:  # 50% chance
        powerup_type = random.choice(["health", "speed", "damage", "shield"])
        # Find valid spawn position
        attempts = 0
        while attempts < 100:
            x = random.randint(100, WIDTH-100)
            y = random.randint(100, HEIGHT-100)
            # Check if position is clear
            if not any(wall.rect.collidepoint(x, y) for wall in walls) and \
               not any(swall.rect.collidepoint(x, y) for swall in small_walls):
                powerup = PowerUp(x, y, powerup_type)
                all_sprites.add(powerup)
                powerups.add(powerup)
                break
            attempts += 1

# Initialize Game
game_manager = GameManager()
all_sprites = pygame.sprite.Group()
zombies = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
gold_bars = pygame.sprite.Group()
powerups = pygame.sprite.Group()
walls = pygame.sprite.Group()
small_walls = pygame.sprite.Group()

# Create initial level
for row_index, row in enumerate(current_level_map):
    for col_index, tile in enumerate(row):
        x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
        if tile == 1:  # Main walls
            wall = Wall(x, y)
            all_sprites.add(wall)
            walls.add(wall)
        elif tile == 2:  # Small walls/obstacles
            sw = SmallWall(x, y)
            all_sprites.add(sw)
            small_walls.add(sw)

# Find a valid spawn position for player
def find_valid_spawn_position():
    """Find a clear position for player to spawn"""
    attempts = 0
    while attempts < 1000:
        x = random.randint(100, WIDTH-100)
        y = random.randint(100, HEIGHT-100)
        
        # Check if position is clear of walls
        player_rect = pygame.Rect(x-20, y-20, 40, 40)  # Player size
        collision = False
        
        # Check collision with main walls
        for wall in walls:
            if player_rect.colliderect(wall.rect):
                collision = True
                break
        
        # Check collision with small walls
        if not collision:
            for small_wall in small_walls:
                if player_rect.colliderect(small_wall.rect):
                    collision = True
                    break
        
        if not collision:
            return x, y
        
        attempts += 1
    
    # Fallback: try center area
    center_x, center_y = WIDTH//2, HEIGHT//2
    player_rect = pygame.Rect(center_x-20, center_y-20, 40, 40)
    collision = False
    
    for wall in walls:
        if player_rect.colliderect(wall.rect):
            collision = True
            break
    
    if not collision:
        for small_wall in small_walls:
            if player_rect.colliderect(small_wall.rect):
                collision = True
                break
    
    if not collision:
        return center_x, center_y
    
    # Last resort: find any open space
    for y in range(50, HEIGHT-50, 50):
        for x in range(50, WIDTH-50, 50):
            player_rect = pygame.Rect(x-20, y-20, 40, 40)
            collision = False
            
            for wall in walls:
                if player_rect.colliderect(wall.rect):
                    collision = True
                    break
            
            if not collision:
                for small_wall in small_walls:
                    if player_rect.colliderect(small_wall.rect):
                        collision = True
                        break
            
            if not collision:
                return x, y
    
    # Ultimate fallback
    return 100, 100

# Spawn player in valid position
player_x, player_y = find_valid_spawn_position()
player = Player(player_x, player_y)
all_sprites.add(player)

# Spawn Initial Enemies
zombie1 = Zombie(800, 300)
zombie2 = Zombie(1000, 500)
ghost1 = Ghost(400, 200)
all_sprites.add(zombie1, zombie2, ghost1)
zombies.add(zombie1, zombie2)
ghosts.add(ghost1)

# Spawn Coins
gold1 = Gold(500, 300)
gold2 = Gold(700, 400)
gold3 = Gold(900, 200)
all_sprites.add(gold1, gold2, gold3)
gold_bars.add(gold1, gold2, gold3)

# Spawn Power-up
powerup1 = PowerUp(600, 600, "speed")
all_sprites.add(powerup1)
powerups.add(powerup1)

# UI Functions
def draw_health_bar(screen, player, x, y):
    """Draw a beautiful health bar"""
    bar_width = 200
    bar_height = 25
    
    # Background
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height), border_radius=12)
    
    # Health fill
    health_ratio = player.health / player.max_health
    health_width = bar_width * health_ratio
    
    # Color based on health
    if health_ratio > 0.6:
        color = (0, 255, 0)  # Green
    elif health_ratio > 0.3:
        color = (255, 255, 0)  # Yellow
    else:
        color = (255, 0, 0)  # Red
    
    pygame.draw.rect(screen, color, (x, y, health_width, bar_height), border_radius=12)
    
    # Border
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 3, border_radius=12)
    
    # Health text
    health_text = f"{player.health}/{player.max_health}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(health_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + bar_width//2, y + bar_height//2))
    screen.blit(text_surface, text_rect)

def draw_coin_counter(screen, coins_collected, required_coins, x, y):
    """Draw coin counter with progress"""
    # Background
    pygame.draw.rect(screen, (50, 50, 50), (x, y, 250, 30), border_radius=15)
    
    # Progress bar
    progress = coins_collected / required_coins if required_coins > 0 else 0
    progress_width = 250 * min(progress, 1.0)
    
    # Color based on progress
    if progress >= 1.0:
        color = (255, 215, 0)  # Gold
    else:
        color = (255, 165, 0)  # Orange
    
    pygame.draw.rect(screen, color, (x, y, progress_width, 30), border_radius=15)
    
    # Border
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 250, 30), 2, border_radius=15)
    
    # Coin text
    coin_text = f"💰 {coins_collected}/{required_coins}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(coin_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + 125, y + 15))
    screen.blit(text_surface, text_rect)

def draw_powerup_indicators(screen, player, x, y):
    """Draw active powerup indicators"""
    y_offset = 0
    if player.speed_boost > 0:
        pygame.draw.rect(screen, (30, 30, 30), (x, y + y_offset, 200, 25), border_radius=12)
        text = f"⚡ Speed Boost: {player.speed_boost}x"
        font = pygame.font.Font(None, 20)
        text_surface = font.render(text, True, (0, 255, 0))
        screen.blit(text_surface, (x + 10, y + y_offset + 5))
        y_offset += 30
    
    if player.damage_boost > 1:
        pygame.draw.rect(screen, (30, 30, 30), (x, y + y_offset, 200, 25), border_radius=12)
        text = f"⚔️ Damage Boost: {player.damage_boost}x"
        font = pygame.font.Font(None, 20)
        text_surface = font.render(text, True, (255, 255, 0))
        screen.blit(text_surface, (x + 10, y + y_offset + 5))
        y_offset += 30
    
    if player.shield_active:
        pygame.draw.rect(screen, (30, 30, 30), (x, y + y_offset, 200, 25), border_radius=12)
        text = "🛡️ Shield Active"
        font = pygame.font.Font(None, 20)
        text_surface = font.render(text, True, (0, 0, 255))
        screen.blit(text_surface, (x + 10, y + y_offset + 5))

# Game Loop
running = True
while running:
    clock.tick(FPS)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_manager.current_state == GameState.PLAYING:
                    game_manager.current_state = GameState.PAUSED
                elif game_manager.current_state == GameState.PAUSED:
                    game_manager.current_state = GameState.PLAYING
                elif game_manager.current_state == GameState.LEVEL_COMPLETE:
                    # Continue to next level
                    game_manager.current_level += 1
                    game_manager.coins_collected = 0
                    game_manager.required_coins = 3 + game_manager.current_level  # Increase difficulty
                    game_manager.current_state = GameState.PLAYING
                    # Reset player health
                    player.health = player.max_health
                    # Clear and respawn entities
                    spawn_new_level()
                elif game_manager.current_state == GameState.GAME_OVER:
                    # Restart game
                    game_manager.current_level = 1
                    game_manager.coins_collected = 0
                    game_manager.required_coins = 3
                    game_manager.score = 0
                    game_manager.current_state = GameState.PLAYING
                    player.health = player.max_health
                    spawn_new_level()

    # Update
    if game_manager.current_state == GameState.PLAYING:
        all_sprites.update()

        # Collision Check (Zombies)
        for zombie in zombies:
            if pygame.sprite.collide_rect(player, zombie):
                if zombie.can_attack(player):
                    if player.take_damage(zombie.damage):
                        game_manager.current_state = GameState.GAME_OVER

        # Collision Check (Ghosts)
        for ghost in ghosts:
            if pygame.sprite.collide_rect(player, ghost):
                if ghost.can_attack(player):
                    if player.take_damage(ghost.damage):
                        game_manager.current_state = GameState.GAME_OVER

        # Collision Check (Gold)
        collected_gold = pygame.sprite.spritecollide(player, gold_bars, True)
        for gold in collected_gold:
            game_manager.coins_collected += gold.value
            game_manager.score += 10

        # Collision Check (Power-ups)
        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in collected_powerups:
            if powerup.powerup_type == "health":
                player.health = min(player.max_health, player.health + powerup.value)
            elif powerup.powerup_type == "speed":
                player.speed_boost = powerup.value
            elif powerup.powerup_type == "damage":
                player.damage_boost = powerup.value
            elif powerup.powerup_type == "shield":
                player.shield_active = True
            game_manager.score += 50

        # Check level completion
        if game_manager.coins_collected >= game_manager.required_coins:
            game_manager.current_state = GameState.LEVEL_COMPLETE

    # Draw
    screen.fill((20, 20, 40))
    
    if game_manager.current_state == GameState.PLAYING:
        all_sprites.draw(screen)
        
        # Draw UI
        draw_health_bar(screen, player, 10, 10)
        draw_coin_counter(screen, game_manager.coins_collected, game_manager.required_coins, 10, 50)
        draw_powerup_indicators(screen, player, 10, 90)
        
        # Score and Level
        draw_text(f"Score: {game_manager.score}", 30, 10, HEIGHT - 60)
        draw_text(f"Level: {game_manager.current_level}", 30, 10, HEIGHT - 30)
        
    elif game_manager.current_state == GameState.PAUSED:
        all_sprites.draw(screen)
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Pause text
        draw_text("PAUSED", 72, WIDTH//2 - 100, HEIGHT//2 - 50)
        draw_text("Press ESC to resume", 36, WIDTH//2 - 150, HEIGHT//2 + 20)
        
    elif game_manager.current_state == GameState.GAME_OVER:
        screen.fill((50, 20, 20))
        draw_text("GAME OVER", 72, WIDTH//2 - 150, HEIGHT//2 - 50)
        draw_text(f"Final Score: {game_manager.score}", 36, WIDTH//2 - 100, HEIGHT//2 + 20)
        draw_text("Press ESC to restart", 24, WIDTH//2 - 100, HEIGHT//2 + 60)
        
    elif game_manager.current_state == GameState.LEVEL_COMPLETE:
        screen.fill((20, 50, 20))
        draw_text("LEVEL COMPLETE!", 72, WIDTH//2 - 200, HEIGHT//2 - 50)
        draw_text(f"Score: {game_manager.score}", 36, WIDTH//2 - 80, HEIGHT//2 + 20)
        draw_text(f"Level {game_manager.current_level} Complete!", 36, WIDTH//2 - 120, HEIGHT//2 + 50)
        draw_text("Press ESC to continue to next level", 24, WIDTH//2 - 150, HEIGHT//2 + 90)
    
    pygame.display.flip()

pygame.quit()