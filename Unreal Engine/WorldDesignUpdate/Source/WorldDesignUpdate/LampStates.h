#pragma once
#include "LightSource.h"

class ALightSource;
class UWorldDesignUpdateGameInstance;

class WORLDDESIGNUPDATE_API LampState {

protected:
    LampState() {}
    virtual ~LampState() {}

public:
    virtual void Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine) = 0;
    virtual LampState* GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine) = 0;

};

class WORLDDESIGNUPDATE_API OffLampState : public LampState {
    
protected:
    OffLampState() {}
    virtual ~OffLampState() {}

public:
    virtual void Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    virtual LampState* GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    static OffLampState* GetInstance();
};

class WORLDDESIGNUPDATE_API OnNearLampState : public LampState {

protected:
    OnNearLampState() {}
    virtual ~OnNearLampState() {}

public:
    virtual void Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    virtual LampState* GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    static OnNearLampState* GetInstance();
};

class WORLDDESIGNUPDATE_API OnLampState : public LampState {

protected:
    OnLampState() {}
    virtual ~OnLampState() {}

public:
    virtual void Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    virtual LampState* GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    static OnLampState* GetInstance();
};

class WORLDDESIGNUPDATE_API AlwaysOnLampState : public LampState {

protected:
    AlwaysOnLampState() {}
    virtual ~AlwaysOnLampState() {}

public:
    virtual void Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    virtual LampState* GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine);
    static AlwaysOnLampState* GetInstance();
};
