from cerebras.cloud.sdk import Cerebras
import os

client = Cerebras(api_key=str(os.environ.get('CEREBRAS_API_KEY')))

def generate_app_name(script):
  stream = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": 'You are a Tech Nerd. The following is a description of a Python Program your friend is writing. no further info will be provided after the initial brief. Carefully Give the program a good name (replace spaces with underscores, no special characters). NO INTROS, NO OUTROS, JUST THE PROGRAM NAME ON A SINGLE LINE.'
          },
          {
              "role":"user",
              "content":script
          }
      ],
      model="qwen-3-32b",
      stream=True,
      max_completion_tokens=4096,
      temperature=0.2,
      top_p=1
  )

  ALL=""
  for chunk in stream:
    ALL+=chunk.choices[0].delta.content or ""
  return ALL
  
def fix_code(code):
  stream = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": 'You are a Python Software Developer. The following is a Python Program your colleague has build, find any bugs present in it and fix them (if any) . Write the new python code complete from start to finish. NO INTROS, NO OUTROS, Just Code.'
          },
          {
              "role":"user",
              "content":code
          }
      ],
      model="qwen-3-32b",
      stream=True,
      max_completion_tokens=12288,
      temperature=0.2,
      top_p=1
  )

  ALL=""
  for chunk in stream:
    ALL+=chunk.choices[0].delta.content or ""
  return ALL


def generate_technical_description(script):
  stream = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": 'You are a Python Software Engineer. The following is a description of a Python Program your client wants you to build, no further info will be provided after the initial brief. Carefully design the program, which will be placed all in a single .py file once written. Dont write Python code, Write a well formatted technical description (detailed but not too long) for the developers to build the program. NO INTROS, NO OUTROS.'
          },
          {
              "role":"user",
              "content":script
          }
      ],
      model="qwen-3-32b",
      stream=True,
      max_completion_tokens=12288,
      temperature=0.2,
      top_p=1
  )

  ALL=""
  for chunk in stream:
    ALL+=chunk.choices[0].delta.content or ""
  return ALL

def generate_sudo_code(script):
  stream = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": 'You are a Python Software Developer. The following is a technical description of a Python Program that the Software Engineer in your team wants you to build, no further info will be provided after the initial description. Carefully design the flow of the program (which function calls which other function, and what each function does), which will be placed all in a single .py file once written. Dont write Python code, Write Sudo Code (breif but not too complicated) for the other developers in your team to build the program. NO INTROS, NO OUTROS.'
          },
          {
              "role":"user",
              "content":script
          }
      ],
      model="qwen-3-32b",
      stream=True,
      max_completion_tokens=12288,
      temperature=0.2,
      top_p=1
  )

  ALL=""
  for chunk in stream:
    ALL+=chunk.choices[0].delta.content or ""
  return ALL

def generate_python_code(script):
  stream = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": 'You are a Python Programmer. The following is the Sudo Code of a Python Program that the Senior Software Developer in your team wants you to build, no further info will be provided after the initial description. Carefully write the Python Program (Follow the Sudo Code given to you), dont think too much. The program will be placed all in a single .py file once written. NO INTROS, NO OUTROS.'
          },
          {
              "role":"user",
              "content":script
          }
      ],
      model="qwen-3-32b",
      stream=True,
      max_completion_tokens=12288,
      temperature=0.2,
      top_p=1
  )

  ALL=""
  for chunk in stream:
    ALL+=chunk.choices[0].delta.content or ""
  return ALL


def generate_app(brief):
  tech_des=generate_technical_description(brief).split("</think>")[1]
  print('t_d')
  sudo_code=generate_sudo_code(tech_des).split("</think>")[1]
  print('s_c')
  python_code=generate_python_code(sudo_code).split("</think>")[1][2:]
  print('p_c')
  python_code=fix_code(python_code).split("</think>")[1][2:]
  print('f_p_c')

  return python_code