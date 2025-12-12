from cerebras.cloud.sdk import Cerebras
import os
import time

client = Cerebras(api_key=str(os.environ.get('CEREBRAS_API_KEY')))



def query_llm(sys_prompt,user_prompt,llm_model="qwen-3-32b",llm_limit=12288,think=False):
    stream = client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": sys_prompt
            },
            {
            "role": "user",
            "content": user_prompt
            }
        ],
        model=llm_model,
        stream=True,
        max_completion_tokens=llm_limit,
        temperature=0.2,
        top_p=1
    )

    ALL=""
    for chunk in stream:
        ALL+=chunk.choices[0].delta.content or ""
    
    thought,answer=ALL.split('</think>')

    if think:
        return thought.replace('<think>','') ,answer[2:]
    else:
        return answer[2:]


def generate_app_name(script):
  sp='You are a Tech Nerd. The following is a description of a Python Program your friend is writing. no further info will be provided after the initial brief. Carefully Give the program a good name (replace spaces with underscores, no special characters). NO INTROS, NO OUTROS, JUST THE PROGRAM NAME ON A SINGLE LINE.'
  return query_llm(sp,script)

def find_bugs(code):
  sp='You are a Python Software Developer. The following is a Python Program your colleague has build, find major bugs present in it (if any) and write solutions for them (do not write any code) and dont add any new features (ignore issues related to long term support and versatility), the goal is to just make the app work, if no issues are found Write "NO ISSUES" , otherwise Write the problem description and a viable solution for them (only 1 sentence per issue). NO INTROS, NO OUTROS.'
  return query_llm(sp,code)

def fix_bugs(code,bugs,brief):
  sp='You are a Python Software Developer. The following is a Python Program your colleague has build, the original brief was "'+brief+'", along with the bugs present in it, fix them using the provided solutions. Write the entire Python Program complete, entirely from start to finish. NO INTROS, NO OUTROS.'
  return query_llm(sp,"//  Faulty Code  //\n\n\n"+code+"\n\n\n//  Bugs and solutions for them  //\n\n\n"+bugs)


def finallize_technical_description(tech_des,brief):
  return query_llm(sp,tech_des)

def generate_technical_description(brief):
  sp= 'You are a Python Software Engineer. The following is a description of a Python Program your client wants you to build, no further info will be provided after the initial brief. Carefully design the program, which will be placed all in a single .py file once written. The implementation should be as simple as possible, avoid external dependencies as much as possible. Dont write Python code, Write a well formatted technical description (detailed but not too long) for the developers to build the program (for every task, include multiple methods of implementation for the devs to choose from). NO INTROS, NO OUTROS.'
  return query_llm(sp,brief)

def generate_sudo_code(script):
  sp= 'You are a Python Software Developer. The following is a technical description of a Python Program that the Software Engineer in your team wants you to build, no further info will be provided after the initial description. Carefully design the flow of the program (which function calls which other function, and what each function does), which will be placed all in a single .py file once written. Dont write Python code, Write Pseudo Code (brief but not too complicated) for the other developers in your team to build the program. NO INTROS, NO OUTROS.'
  return query_llm(sp,script)

def generate_python_code(script):
  sp='You are a Python Programmer. The following is the Pseudo Code of a Python Program that the Senior Software Developer in your team wants you to build, no further info will be provided after the initial description. Carefully write the Python Program (Follow the Sudo Code given to you), dont think too much. The program will be placed all in a single .py file once written. NO INTROS, NO OUTROS.'
  return query_llm(sp,script)

def generate_app(brief):
  tech_des=generate_technical_description(brief).split("</think>")[1]
  print('t_d_I')
  tech_des=finallize_technical_description(tech_des,brief).split("</think>")[1]
  print('t_d_F')
  sudo_code=generate_sudo_code(tech_des).split("</think>")[1]
  print('s_c')
  python_code=generate_python_code(sudo_code).split("</think>")[1][2:]
  print('p_c')
  
  x=0
  while x<2:
    x+=1
    time.sleep(1)
    bugs=find_bugs(python_code).split("</think>")[1][2:]
    print(bugs)
    if "NO ISSUES" in bugs:
      break
    python_code=fix_bugs(python_code,bugs,brief).split("</think>")[1][2:]
  return python_code

