using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnManager : MonoBehaviour
{
    private float spawnRange = 9;

    public GameObject enemyPrefab;
    public List<GameObject> enemies;
    public List<GameObject> powerUps;
    public GameObject powerUpPrefab;
    public int enemyCount;
    public int waveNumber = 1;
    public 

    // Start is called before the first frame update
    void Start()
    {
        SpawnEnemyWave(waveNumber);

    }

    // Update is called once per frame
    void Update()
    {
        enemyCount = FindObjectsOfType<Enemy>().Length;
        if (enemyCount == 0)
        {
            waveNumber++;
            SpawnEnemyWave(waveNumber);
            Instantiate(GetRandomPowerUp(), GenerateSpawnPosition(), powerUpPrefab.transform.rotation);
        }
    }

    void SpawnEnemyWave(int enemiesToSpawn)
    {
        for (int i = 0; i < enemiesToSpawn; i++)
        {
            Instantiate(enemyPrefab, GenerateSpawnPosition(), enemyPrefab.transform.rotation);
        }
    }

    private Vector3 GenerateSpawnPosition()
    {
        float spawnPosX = Random.Range(-spawnRange, spawnRange);
        float spawnPosZ = Random.Range(-spawnRange, spawnRange);
        Vector3 randomPos = new Vector3(spawnPosX, 0, spawnPosZ);
        return randomPos;
    }

    private GameObject GetRandomPowerUp()
    {
        int randomIndex = Random.Range(0, powerUps.Count);
        return powerUps[randomIndex];
    }
}
