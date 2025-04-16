using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FarmableSpawner : MonoBehaviour
{
    public GameObject barrelPrefab;

    public float TimeToSpawn = 7;

    private SpawnLocation[] SpawnPositions;
    private static System.Random Rand = new System.Random();

    // Start is called before the first frame update
    void Start()
    {
        SpawnPositions = FindObjectsByType<SpawnLocation>(FindObjectsSortMode.None);

        // coroutine
        StartCoroutine(SpawnCollectibles());
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private IEnumerator SpawnCollectibles()
    {
        // loop
        while (true)
        {
            // pick a location
            SpawnLocation spawnPoint = PickRandomSpawnLocation();

            if (spawnPoint != null)
            {
                BarrelController collectible = FarmablePool.GetInstance().GetBarrel(spawnPoint.gameObject.transform.position, Quaternion.identity);
                //Instantiate(barrelPrefab, spawnPoint.gameObject.transform.position, Quaternion.identity);
                spawnPoint.SetSpawnObject(collectible.GetComponent<SpawnObject>());
            }
            // wait
            yield return new WaitForSeconds(TimeToSpawn);
        }

    }

    private SpawnLocation PickRandomSpawnLocation()
    {
        // what if already used?
        // what if they are all used?
        // what if no points?

        if (SpawnPositions.Length == 0)
        {
            return null;
        }


        int pos = Rand.Next(SpawnPositions.Length);
        int start = pos;

        if (SpawnPositions[pos].GetSpawnObject() == null)
        {
            return SpawnPositions[pos];
        }

        pos = (pos + 1) % SpawnPositions.Length;

        while (start != pos && SpawnPositions[pos].GetSpawnObject() != null)
        {
            pos = (pos + 1) % SpawnPositions.Length;
        }

        if (start != pos)
        {
            return SpawnPositions[pos];
        }

        return null;
    }
}
