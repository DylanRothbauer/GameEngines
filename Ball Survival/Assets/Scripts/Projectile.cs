using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Projectile : PowerUp
{
    public GameObject projectilePrefab;

    private float speed = 5.0f;
    
    public override void Activate(Collision collision)
    {
        Debug.Log("PROJECTILE ACTIVATE");

        // Instanciate bullets to go in all directions
        //Instantiate(projectilePrefab, gameObject.transform.position, projectilePrefab.transform.rotation);
    }
}
