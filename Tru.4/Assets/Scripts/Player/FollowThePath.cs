using UnityEngine;

public class FollowThePath : MonoBehaviour
{

    public GameObject[] waypoints;

    [SerializeField]
    private float moveSpeed = 1f;

    //[HideInInspector]
    public int waypointIndex = 0;

    public bool moveAllowed = false;

    private EventSystem NowEvent;

    // Use this for initialization
    private void Start()
    {
        transform.position = waypoints[waypointIndex].transform.position;
        moveAllowed = false;
    }

    // Update is called once per frame
    private void Update()
    {
        if (moveAllowed)
            Move();
    }

    private void Move()
    {
        if (waypointIndex <= waypoints.Length - 1)
        {
            transform.position = Vector2.MoveTowards(transform.position,
            waypoints[waypointIndex].transform.position,
            moveSpeed * Time.deltaTime);

            if (transform.position == waypoints[waypointIndex].transform.position)
            {
                waypointIndex += 1;
            }
        }
    }
}
