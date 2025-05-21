using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pushback : PowerUp
{

    public override void Activate(Collision collision)
    {
        Rigidbody enemyRigidbody = collision.gameObject.GetComponent<Rigidbody>();
        Vector3 awayFromPlayer = collision.gameObject.transform.position - transform.position;
        enemyRigidbody.AddForce(awayFromPlayer * powerUpStrength, ForceMode.Impulse);
    }
}
