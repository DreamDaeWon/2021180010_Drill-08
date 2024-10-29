from pico2d import load_image, get_time

from Lecture10_Character_Controller_1.state_machine import time_out, space_down, right_down, left_up, left_down, right_up, down_a, up_a
from state_machine import StateMachine


class Idle:
    @staticmethod
    def enter(boy,e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.dir = -1
        elif right_up(e) or  left_down(e):
            boy.action = 3
            boy.dir = 1

        # 현재 시간을 저장
        if boy.dir == -1:
            boy.action = 2

        elif boy.dir == 1:
            boy.action = 3

        boy.start_time = get_time()
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT',0))


    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.dir,boy.action = -1, 3
        elif right_up(e) or left_down(e):
            boy.dir, boy.action = 1, 2
        pass

    @staticmethod
    def exit(boy,e):

        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):

        if boy.dir == -1:
            boy.image.clip_composite_draw(
                boy.frame *100, 300, 100, 100,
                3.141592/2, # 90도 회전
                'v', # 좌우상하 반전 X
                boy.x + 25, boy.y - 25, 100, 100
            )
        else:
            boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100,
                3.141592 / 2,  # 90도 회전
                '',  # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )


class Run:
    @staticmethod
    def enter(boy,e):
        if left_up(e) or right_down(e):
            boy.dir,boy.action = 1, 1
        elif right_up(e) or left_down(e):
            boy.dir, boy.action = -1, 0

        boy.frame = 0


        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class AutoRun:
    @staticmethod
    def enter(boy,e):

        boy.dir = 1
        if boy.dir == 1:
            boy.action = 1
        elif boy.dir == -1:
            boy.action = 0



        boy.start_time = get_time()
        boy.frame = 0



        pass

    @staticmethod
    def exit(boy,e):

        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 50
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.start_time >= 5:
            boy.state_machine.add_event(('TIME_OUT',0))

        if boy.x + 100 >= 800:
            if boy.dir == 1:
                boy.dir = -1
                boy.action = 0

        if boy.x - 100 <= 0:
            if boy.dir == -1:
                boy.dir = 1
                boy.action = 1

        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + 170,600,600)
        pass







class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 state machine 생성
        self.state_machine.start(Idle) # 초기 상태가 Idle
        self.state_machine.set_transitions({
            Idle : {down_a : AutoRun, up_a : AutoRun, right_down : Run, left_down : Run, right_up : Run, left_up : Run, time_out : Sleep},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},  # 런 상태에서 가만히 있겠다.
            Sleep : {right_down : Run, left_down : Run, right_up : Run, left_up : Run, space_down : Idle},
            AutoRun : {down_a : AutoRun, up_a : AutoRun, right_down : Run, left_down : Run, right_up : Run, left_up : Run, time_out : Idle}
        })
        self.start_time = get_time()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : 입력 이벤트 key mouse
        # 우리가 state machine 전달해줄거는 (,)
        self.state_machine.add_event(('INPUT',event))

        pass

    def draw(self):
        self.state_machine.draw()
