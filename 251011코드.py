import time
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt
font_path = "C:/Windows/Fonts/malgun.ttf"

fontprop = fm.FontProperties(fname=font_path)
mpl.rc('font', family=fontprop.get_name())


fig, axs = plt.subplots(1, 2, figsize=(10, 5))

print("오늘 공부할 과목의 수를 입력하세요:")
labels2 = []
sizes2 = []
subjects = int(input())

for i in range(subjects):
    subject_name = input(f"{i+1}번째 과목 이름을 입력하세요: ")
    subject_list=[]
    subject_list.append(subject_name)
    percent = float(input(f"{subject_name}의 비율(%)을 입력하세요: "))
    percent_list=[]
    percent_list.append(percent)
    labels2.append(subject_name)
    sizes2.append(percent)

def make_potato(labels):
    def my_potato(pct):
        total = sum(sizes2)
        value = pct * total / 100.0
        label = labels[my_potato.index]
        my_potato.index += 1
        return f"{label}\n{value:.1f}%"
    my_potato.index = 0
    return my_potato

axs[1].pie(
    sizes2,
    labels=labels2,
    autopct=make_potato(labels2),
    startangle=90
)
axs[1].set_title("과목별 공부 시간 비율")
axs[1].axis('equal')

print("일일 공부량을 입력하세요(분):")
daily_goal = input()
total_elapsed_sec = 0
print("오늘의 목표 공부 시간은 " + daily_goal + "분입니다.")
print("\n공부를 시작하려면 엔터를 누르세요.")
if input() == "":
    print("공부를 시작합니다.")
start_time = time.time()

print("공부를 잠시 멈추려면 엔터를 누르세요.")
if input() == "":
    print("공부를 일시정지합니다.")
    pause_time = time.time()
    study_duration = pause_time - start_time
    total_elapsed_sec += study_duration

    print("공부를 다시 시작하려면 엔터를 누르세요.")
    if input() == "":
        print("공부를 다시 시작합니다.")
        start_time = time.time()

print("공부를 종료하려면 엔터를 누르세요.")
input()
end_time = time.time()
final_study_duration = end_time - start_time
total_elapsed_sec += final_study_duration

elapsed_sec = int(total_elapsed_sec)
minutes = elapsed_sec // 60
seconds = elapsed_sec % 60

print("공부가 종료되었습니다.")
print("총 공부 시간:", minutes, "분", seconds, "초")

try:
    goal = int(daily_goal)
    goal_sec = 60 * goal
    result = (elapsed_sec * 100) / goal_sec

    if elapsed_sec >= goal_sec:
        print("목표 달성! 축하해요!! :)")
    else:
        print("아쉽지만 목표를 달성하지 못했어요ㅠㅠ 목표 달성률은", round(result, 2), "%에요.")
except:
    print("오류가 발생했습니다! 입력 값에 문제가 없는지 한번 더 확인해보세요.")
index=int(subjects+1)
if index <len(subject_list):
    for i in range(index+1):
        if total_elapsed_sec>=goal_sec*int(percent_list[index]):
            print(f"{subject_list[i]} 과목 목표 달성! 축하해요!! :)")
            
time.sleep(5)
st = round(result, 2)
abels1 = ['총 공부 시간', '남은 목표 시간']
sizes1 = [st, 100 - st]

def make_pumpkin(labels):
    def my_pumpkin(pct):
        total = sum(sizes1)
        value = pct * total / 100.0
        label = labels[my_pumpkin.index]
        my_pumpkin.index += 1
        return f"{label}\n{value:.1f}%"
    my_pumpkin.index = 0
    return my_pumpkin

axs[0].pie(
    sizes1,
    labels=abels1,
    autopct=make_pumpkin(abels1),
    startangle=90
)
axs[0].set_title("공부 목표 달성률")
axs[0].axis('equal')

plt.tight_layout()
plt.show()
time.sleep(3)
