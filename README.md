# PBL5 - Body Posture Detection

## 1. Tech Stack

- CameraSocket: C/C++
- WebApp: Python (Django)

## 2. Branch

- `main`: stable build branch
- `dev`: development branch
- `dev-camerasocket`: dev branch for camerasocket (merge to `dev`)
- `dev-webapp`: dev branch for webapp (merge to `dev`)
## 3. Flow

![img](./assets/BasicFlow.png)

**Brief:** Camera on -> Socket Client Sending Event to Server -> Server Model Frame Handling -> Prediction Result Sending Back Event -> Showing Live Result

## 4. Todo List

* [ ] Camera Socket
* [ ] WebApp
* [X] Models (Current: [best_model.resolved.h5](./_models/best_model.resolved.h5)).

---

# License
