# NetCoach
Utility to graph training progress in large networks 
author: Jay Hack (jhack@palantir.com)

## Usage
- Start training a model
- Whenever you feel the need, hit a hook with the following info:
    - model name (string)
    - model loss (float)
    - model iteration (optional)
- Hit up the training server to see how it is doing 

## Future Extensions
- Add ability to save models themselves (if small)

## Terminology
- Series: training loss
