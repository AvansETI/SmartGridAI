1. Login to wandb with github
2. Get added to team
3. Add weights and biases
```
pip install --upgrade wandb
```
4. Go to settings and copy the API key
5. Login to wandb with API key
```
wandb login ${API_key}
```
6. In wandb folder in the project add the following line under default
```
entity = smart_grid
```
7. Make a new project in the group
8. Add wandb code to project 

```
import wandb
from wandb.keras import WandbCallback
wandb.init(project="${projectName}")
```
9. glhf