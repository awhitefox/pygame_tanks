import pygame
from tanks.constants import PIXEL_RATIO
from tanks.directions import *
from tanks.grid import get_rect
from tanks.time import delta_time
from tanks.sprites import GridSpriteBase, Shell
from tanks.images import load_image, cut_sheet
from tanks.sounds import load_sound


class Tank(pygame.sprite.Sprite):
    """탱크 클래스"""
    distance_to_animate = PIXEL_RATIO * 2
    shell_spawn_offset = PIXEL_RATIO
    shoot_cooldown = 1
    speed = 150
    s_speed = 400
    point = 0

    

    #탱크 사운드, 이미지
    shoot_sound = load_sound('tank_fire.flac')
    explosion_sound = load_sound('tank_explosion.flac')

    frames = cut_sheet(load_image('tanks.png'), 8, 2)


    def __init__(self, x: float, y: float, is_default_player: bool, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        x, y = x + PIXEL_RATIO, y + PIXEL_RATIO  # center tank in 2x2 square
        self.distance = 0
        self.seconds_from_last_shot = self.shoot_cooldown
        self.frame = 0
        self.pos = pygame.Vector2(x, y)
        if is_default_player:
            self.control_scheme = TankControlScheme.default()
            self.images = self.frames[:8]
            self.direction = NORTH
        else:
            self.control_scheme = TankControlScheme.alternative()
            self.images = self.frames[8:]
            self.direction = SOUTH
        self.image = self._get_image()
        self.rect = self.image.get_rect()
        # resize rect because tank is smaller
        self.rect.inflate_ip(-2 * PIXEL_RATIO, -2 * PIXEL_RATIO)
        self.rect.x = x
        self.rect.y = y

        self.movement = None

        self.vector_velocity = pygame.Vector2(0, 0)

    def update(self) -> None:
        field = get_rect()

        self.movement = self.control_scheme.get_movement()
        self.seconds_from_last_shot += delta_time()

        if self.control_scheme.shoot_pressed():
            if self.seconds_from_last_shot >= self.shoot_cooldown:
                self.shoot(self.s_speed)
                self.seconds_from_last_shot = 0
                return

        if self.movement is not None:
            self.direction = self.movement

        self.image = self._get_image()
        velocity_vec = direction_to_vector(self.movement, self.speed) * delta_time()

        new_pos = self.pos + velocity_vec
        new_rect = pygame.Rect(new_pos.x, new_pos.y, *self.rect.size)

        for group in self.groups():
            for sprite in group:
                if sprite is not self and new_rect.colliderect(sprite.rect):
                    if (isinstance(sprite, GridSpriteBase) and sprite.tank_obstacle) \
                            or isinstance(sprite, Tank):
                        return
                    if isinstance(sprite, Shell) :
                        self.kill()
                        sprite.kill()
                        return
                    if (isinstance(sprite, GridSpriteBase) and sprite.die_obstacle) :
                        self.kill()
                        return
                    if (isinstance(sprite, GridSpriteBase) and sprite.speed_up):
                        self.speedup()
                        sprite.kill()
                        return
                    if (isinstance(sprite, GridSpriteBase) and sprite.s_speedup):
                        self.s_speed += 50
                        sprite.kill()
                        return
                    ###################################
                    if (isinstance(sprite, GridSpriteBase) and sprite.range):
                        Shell.shootrange += 50
                        sprite.kill()
                        return
                    #######################################33
                    if (isinstance(sprite, GridSpriteBase) and sprite.pointup):
                        sprite.kill()
                        self.point += 10
                        print(self.point)
                        return
        if new_rect.x + self.rect.size[0] > field.right or new_rect.x < field.left \
                or new_rect.y + self.rect.size[1] > field.bottom or new_rect.y < field.top:
            return

        self.distance += (new_pos - self.pos).length()
        self.pos = new_pos
        self.rect = new_rect

    def point_up(self) -> None:
        self.point = self.point + 100

    def speedup(self) -> None:
            self.speed = self.speed + 30

    def shoot(self, s_speed: int) -> None:
        """샷 초기화 방법"""
        off = self.shell_spawn_offset
        pos = None
        if self.direction == NORTH:
            pos = self.pos.x + (self.rect.w / 2), self.pos.y - off
        elif self.direction == SOUTH:
            pos = self.pos.x + (self.rect.w / 2), self.pos.y + self.rect.h + off
        elif self.direction == WEST:
            pos = self.pos.x - off, self.pos.y + self.rect.h / 2
        elif self.direction == EAST:
            pos = self.pos.x + self.rect.w + off, self.pos.y + self.rect.h / 2
        Shell(s_speed, *pos, self.direction, *self.groups())
        self.shoot_sound.play()
    
    def mirror_shoot(self, s_speed: int) -> None:
        """샷 초기화 방법"""
        off = self.shell_spawn_offset
        pos = None
        if self.direction == NORTH:
            pos = self.pos.y + self.rect.h + off, self.pos.x + (self.rect.w / 2)
        elif self.direction == SOUTH:
            pos = self.pos.y - off, self.pos.x + (self.rect.w / 2)
        elif self.direction == WEST:
            pos = self.pos.y + self.rect.h / 2, self.pos.x + self.rect.w + off, 
        elif self.direction == EAST:
            pos = self.pos.y + self.rect.h / 2, self.pos.x - off
        Shell(s_speed, *pos, self.direction, *self.groups())
        self.shoot_sound.play()

    def kill(self) -> None:
        self.explosion_sound.play()
        super().kill()

    def _get_image(self) -> pygame.Surface:
        """탱크가 보는 방향을 기준으로 사진을 얻는 보호 방법"""
        frame = 0
        if self.distance > self.distance_to_animate:
            self.frame += 1 if self.frame % 2 == 0 else -1
            self.distance = 0

        if self.direction == NORTH:
            frame = 0
        elif self.direction == SOUTH:
            frame = 4
        elif self.direction == WEST:
            frame = 2
        elif self.direction == EAST:
            frame = 6

        if self.frame % 2 == 1:
            frame += 1
        self.frame = frame
        return self.images[self.frame]


class TankControlScheme:
    """탱크 제어 회로 클래스"""
    def __init__(self, up: int, right: int, down: int, left: int, shoot: int):
        self._up = up
        self._right = right
        self._down = down
        self._left = left
        self._shoot = shoot

    def get_movement(self) -> int:
        """키를 눌러 방향을 얻는 방법"""
        if pygame.key.get_pressed()[self._up]:
            return NORTH
        elif pygame.key.get_pressed()[self._right]:
            return EAST
        elif pygame.key.get_pressed()[self._down]:
            return SOUTH
        elif pygame.key.get_pressed()[self._left]:
            return WEST

    def shoot_pressed(self) -> bool:
        """샷 버튼 확인"""
        return pygame.key.get_pressed()[self._shoot]

    @classmethod
    def default(cls) -> 'TankControlScheme':
        """첫 번째 플레이어의 컨트롤 키를 사용하여 TankControlScheme 클래스 개체 생성
        (WASD - 모션, 스페이스바 - 샷)"""
        return cls(pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_SPACE)

    @classmethod
    def alternative(cls) -> 'TankControlScheme':
        """두 번째 플레이어의 컨트롤 키를 사용하여 TankControlScheme 클래스 개체 생성
        (화살표 이동, 입력 - 샷)"""
        return cls(pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RETURN)
