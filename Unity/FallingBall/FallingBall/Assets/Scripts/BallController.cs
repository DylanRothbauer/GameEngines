using UnityEngine;

public class BallController : MonoBehaviour
{
    public float launchSpeed = 80f;
    public bool isLaunched = false;
    public float cornerBoost = 5f;
    public float stopThreshold = 0.2f; // Velocity below this will be zeroed

    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true; // ball starts paused
        rb.linearDamping = 0f;
        rb.angularDamping = 0f;
    }

    void Update()
    {
        if (!isLaunched && Input.GetKeyDown(KeyCode.Space))
        {
            LaunchBall();
        }
    }

    void LaunchBall()
    {
        isLaunched = true;
        rb.isKinematic = false;
        // Launch diagonally down-right
        rb.linearVelocity = new Vector3(launchSpeed, 5.0f, 0);
    }

    void OnCollisionEnter(Collision collision)
    {
        if (!collision.gameObject.CompareTag("Step"))
            return;

        Collider col = collision.collider;
        Bounds b = col.bounds;

        Vector3 incomingVel = rb.linearVelocity;

        bool cornerHit = false;

        foreach (ContactPoint contact in collision.contacts)
        {
            Vector3 normal = contact.normal;
            float x = contact.point.x;

            float edgeThreshold = 0.7f;

            bool nearLeftEdge  = Mathf.Abs(x - b.min.x) < edgeThreshold;
            bool nearRightEdge = Mathf.Abs(x - b.max.x) < edgeThreshold;

            float horizontalSpeed = Mathf.Abs(incomingVel.x);

            bool hasSideMotion = horizontalSpeed > 2f;   // important
            bool notPurelyFlat = normal.y < 0.90f;       // allow slight flatness

            if ((nearLeftEdge || nearRightEdge) && hasSideMotion && notPurelyFlat)
            {
                cornerHit = true;
                break;
            }
        }

        if (cornerHit)
        {
            rb.linearVelocity += new Vector3(cornerBoost, cornerBoost, 0);
            Debug.Log("Corner boost!");
        }
        else
        {
            // Strong flat braking
            Vector3 v = rb.linearVelocity;

            v.x *= 0.5f;  // very aggressive slowdown

            rb.linearVelocity = new Vector3(v.x, rb.linearVelocity.y, 0);
        }
    }


    void OnCollisionStay(Collision collision)
    {
        if (!collision.gameObject.CompareTag("Step"))
            return;

        Vector3 normal = collision.contacts[0].normal;

        // Flat surface
        if (normal.y > 0.9f)
        {
            Vector3 v = rb.linearVelocity;
            v.x *= 0.90f; // gradual slowdown

            // If very slow, hard stop
            if (Mathf.Abs(v.x) < stopThreshold)
            {
                v.x = 0f;
            }

            rb.linearVelocity = new Vector3(v.x, rb.linearVelocity.y, 0);
        }
    }

}
