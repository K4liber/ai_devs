# ai_devs

### Python environment
1. `conda env create -f environment.yml --prefix=/usr/local/lib/anaconda3/envs/ai_devs`  
2. `conda activate /usr/local/lib/anaconda3/envs/ai_devs`
3. `conda env update -f environment.yml --prefix=/usr/local/lib/anaconda3/envs/ai_devs`
### Task steps
1. Set the task name in the `.envs` file
2. Set token: `python script/task.py set_token`  
3. Print task: `python script/task.py print_task`   
4. Answer with string: `python script/task.py answer_with_str <answer_str>`  
