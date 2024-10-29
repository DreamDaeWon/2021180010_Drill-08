# 이벤트 체크 함수 정의
# 상태 이벤트 e = (종류, 실제값)  튜플로 정의
from tkinter.ttk import Label

from sdl2 import SDL_KEYDOWN,SDL_KEYUP, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDLK_a


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e): # e가 time out 인지 판단
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT



def down_a(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def up_a(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a



class StateMachine:
    def __init__(self, obj):
        self.obj = obj # 어떤 객체를 위한 상태머신인지 알려줌. obj = boy.self

        self.event_q = [] # 상태 이벤트를 보관할 리스트

        pass


    def start(self, state):
        self.cur_state = state # 시작 상태를 받아서, 그걸로 현재 상태를 정의
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'Enter into {state}')
        pass

    def update(self):
        self.cur_state.do(self.obj) # Idle.do()

        if self.event_q: # 리스트에 무엇인가 원소가 있으면 true 없으면 false
            e = self.event_q.pop(0)
            # 이 시점에서 우리한테 주어진 정보는?
            # e
            # cur_state
            # 현재 상태와 현재 발생한 이벤트에 따라서 다음상태 하는 법은?


            # 상태변환 테이블을 이용하자
            # 상태변환 테이블?

            for check_e, next_state in self.transitions[self.cur_state].items():
                if check_e(e):
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj, e)
                    self.cur_state = next_state
                    print(f'Enter into {self.cur_state}')
                    self.cur_state.enter(self.obj, e) # 상태 변환의 이유를 찾아주어야 함
                    return # 제대로 이벤트에 따른 상태 변환 완료

            # 이 시점으로 왔다는 것은, event에 따른 전환 못함.
            print(f'        WARNING: {e} not handled at state {self.cur_state}')

        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e):
        print(f'    DEBUG: add event {e}')
        self.event_q.append(e)
        pass

    def set_transitions(self, transitions):

        self.transitions = transitions
        pass