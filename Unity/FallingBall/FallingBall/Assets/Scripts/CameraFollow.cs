using UnityEngine;

public class CameraFollow : MonoBehaviour
{

    public Transform target; // The ball
    public float smoothSpeed = 0.05f;
    public float yOffset = 0f;

    private Vector3 velocity = Vector3.zero;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void LateUpdate()
    {
        if (!target) return;

        // Target position we want the camera to move to
        float cameraYSmoothness = 0.01f;
        float newY = Mathf.Lerp(transform.position.y, target.position.y, cameraYSmoothness);
        transform.position = new Vector3(target.position.x, newY, transform.position.z);
    }
}
