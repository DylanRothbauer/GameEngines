using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BarrelStateMachine : MonoBehaviour
{

    public float v; // time since last visit
    public bool visited = false; // if it was visited since the last frame | visited
    public float t; // total "ripping" time
    public float vTime = 5.0f; // time to grow between visits
    public float tTime = 10.0f; // time to ripen

}
