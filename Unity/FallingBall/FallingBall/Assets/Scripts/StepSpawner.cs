using System.Collections.Generic;
using UnityEngine;

public class StepSpawner : MonoBehaviour
{
    public GameObject stepPrefab;
    public GameObject startingStep;
    public Transform stepParent;
    public Transform ball;
    public float startOffsetY = -1.2f;

    public float stepHeight = 0.6f;
    public float minOffsetX = 6.0f;
    public float maxOffsetX = 6.0f;

    public int stepsAhead = 15;
    public float deleteDistance = 6f;

    private Vector2 lastSpawnPosition;
    private Queue<GameObject> activeSteps = new Queue<GameObject>();

    void Start()
    {
        lastSpawnPosition = new Vector2(startingStep.transform.position.x, startingStep.transform.position.y - startingStep.transform.localScale.y / 2);

        for (int i = 0; i < stepsAhead; i++)
        {
            SpawnStep();
        }
    }

    void Update()
    {
        // Spawn more steps below if needed
        if (lastSpawnPosition.y > ball.position.y - stepsAhead * stepHeight)
        {
            SpawnStep();
        }

        CleanupSteps();
    }

    void SpawnStep()
    {
        // Step moves right naturally
        float offsetX = Random.Range(minOffsetX, maxOffsetX); // always positive
        float offsetY = stepHeight; // vertical spacing = height of step

        Vector2 newPos = new Vector2(
            lastSpawnPosition.x + offsetX,        // move right from last step
            lastSpawnPosition.y - offsetY / 2         // move down by step height
        );

        GameObject step = Instantiate(stepPrefab, newPos, Quaternion.identity, stepParent);
        activeSteps.Enqueue(step);

        lastSpawnPosition = newPos;
    }

    void CleanupSteps()
    {
        while (activeSteps.Count > 0)
        {
            GameObject step = activeSteps.Peek();

            if (step.transform.position.y > ball.position.y + deleteDistance)
            {
                activeSteps.Dequeue();
                Destroy(step);
            }
            else
            {
                break;
            }
        }
    }
}
