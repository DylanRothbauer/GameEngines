using Cainos.PixelArtTopDown_Basic;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using Unity.VisualScripting;
using UnityEngine;

public class FarmablePool : MonoBehaviour
{
    private static FarmablePool instance;
    private Stack<BarrelController> barrels;
    private TopDownCharacterController player;

    public GameObject barrelPrefab;

    

    public static FarmablePool GetInstance()
    {
        return instance;
    }

    private void Awake()
    {
        // check if the instance exists
        if (instance != null && instance != this)
        {
            Destroy(this);
            return;
        }


        // setup
        instance = this;
        barrels = new Stack<BarrelController>();
    }
    // Start is called before the first frame update
    void Start()
    {
        /*player = GameObject.FindWithTag("Player").GetComponent<TopDownCharacterController>();
        player.AddOnItemPickup(ItemPickup);*/
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public BarrelController GetBarrel(Vector3 position, Quaternion rotation)
    {
        GameObject barrel;

        // have a projectile
        if (barrels.Count > 0)
        {
            Debug.LogWarning("Popping Barrel " + barrels.Count);
            barrel = barrels.Pop().gameObject;
            // set up
            barrel.transform.position = position;
            barrel.transform.rotation = rotation;

            // Listen to it
            barrel.GetComponent<BarrelController>().AddOnBarrelStateChange(BarrelUpdate);

            barrel.SetActive(true);
        }
        else
        {
            // don't have a barrel
            barrel = Instantiate(barrelPrefab, position, rotation);

            // Listen to it
            barrel.GetComponent<BarrelController>().AddOnBarrelStateChange(BarrelUpdate);

            Debug.LogWarning("Creating Barrel ");

        }
        return barrel.GetComponent<BarrelController>();
    }

    public void ReturnBarrel(BarrelController barrel)
    {
        Debug.Log("RETURN BARREL");

        // break links
        SpawnObject spawn = barrel.GetComponent<SpawnObject>();
        if (spawn.GetSpawnLocation() != null)
        {
            spawn.GetSpawnLocation().SetSpawnObject(null);
        }
        // destroy it
        //Destroy(barrel.gameObject);

        // Remove method from delegate
        barrel.GetComponent<BarrelController>().RemoveOnBarrelStateChange(BarrelUpdate);

        // hide it
        barrel.gameObject.SetActive(false);

        // Change state to start
        barrel.ResetBarrel();

        // push onto stack
        barrels.Push(barrel);

        Debug.LogWarning("Pushing Barrel " + barrels.Count);

    }

    public void BarrelUpdate(BarrelController barrel, BarrelStates current, BarrelStates next)
    {
        if (current.GetType() == typeof(Dead) && !barrel.IsCoroutineRunning)
        {
            barrel.IsCoroutineRunning = true;
            StartCoroutine(ReturnDeadBarrel(barrel));
        }
    }

    private IEnumerator ReturnDeadBarrel(BarrelController barrel)
    {
        Debug.LogWarning("Starting ReturnDeadBarrel Coroutine for " + barrel.name);
        yield return new WaitForSeconds(3.0f);

        Debug.LogWarning("Calling ReturnBarrel for " + barrel.name);

        // Remove from world and return to cache
        ReturnBarrel(barrel);

        // Reset flag
        barrel.IsCoroutineRunning = false;


    }

    
}
