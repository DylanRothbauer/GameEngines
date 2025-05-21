using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnLocation : MonoBehaviour
{
    private SpawnObject spawnObject;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public SpawnObject GetSpawnObject()
    {
        return spawnObject;
    }

    public void SetSpawnObject(SpawnObject obj)
    {
        // break obj -> me
        if (spawnObject != null)
        {
            spawnObject.SetSpawnLocation(null);
        }
        // is it occupied?

        // break me -> obj
        // set me -> new obj
        spawnObject = obj;

        // set new obj -> me
        if (obj != null)
        {
            if (obj.GetSpawnLocation() != null)
            {
                obj.GetSpawnLocation().SetSpawnObject(null);
            }
            obj.SetSpawnLocation(this);
        }



    }
}
