using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BarrelModel : MonoBehaviour
{

    private int value = 1;

    public BarrelStates currentState;
    public BarrelStateMachine stateValues;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public int getValue()
    {
        return value;
    }

    public void setValue(int value)
    {
        this.value = value;
    }
}
