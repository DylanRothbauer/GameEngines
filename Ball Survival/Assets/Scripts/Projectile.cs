using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Projectile : PowerUp
{
    public override void Activate(Collision collision)
    {
        Debug.Log("PROJECTILE ACTIVATE");
    }
}
