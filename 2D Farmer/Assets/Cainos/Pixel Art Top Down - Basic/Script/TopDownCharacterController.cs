using System.Collections;
using System.Collections.Generic;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;

namespace Cainos.PixelArtTopDown_Basic
{
    public delegate void OnItemPickup(BarrelModel model);

    public class TopDownCharacterController : MonoBehaviour
    {

        public float speed;
        public int itemsPickup = 0;
        public int totalScore = 0;
        public OnItemPickup onItemPickup;

        private Animator animator;
        private BarrelModel model;
        private GameObject canvas;
        

        private void Start()
        {
            animator = GetComponent<Animator>();
            canvas = GameObject.Find("Canvas");
            AddOnItemPickup(ItemPickup);
        }


        private void Update()
        {
            Vector2 dir = Vector2.zero;
            if (Input.GetKey(KeyCode.A))
            {
                dir.x = -1;
                animator.SetInteger("Direction", 3);
            }
            else if (Input.GetKey(KeyCode.D))
            {
                dir.x = 1;
                animator.SetInteger("Direction", 2);
            }

            if (Input.GetKey(KeyCode.W))
            {
                dir.y = 1;
                animator.SetInteger("Direction", 1);
            }
            else if (Input.GetKey(KeyCode.S))
            {
                dir.y = -1;
                animator.SetInteger("Direction", 0);
            }

            dir.Normalize();
            animator.SetBool("IsMoving", dir.magnitude > 0);

            GetComponent<Rigidbody2D>().velocity = speed * dir;
        }


        public void AddOnItemPickup(OnItemPickup listener)
        {
            onItemPickup += listener;
        }

        public void RemoveOnItemPickup(OnItemPickup listener)
        {
            onItemPickup -= listener;
        }

        public void ItemPickup(BarrelModel model)
        {
            Debug.LogWarning("ITEM PICKUP (PLAYER DELEGATE)");
            itemsPickup++;
            totalScore += model.getValue();

            // Update UI
            Transform itemsPickupTransform = canvas.GetComponentInChildren<Canvas>().transform.GetChild(0);
            Transform totalScoreTransform = canvas.GetComponentInChildren<Canvas>().transform.GetChild(1);

            if (itemsPickupTransform != null && totalScoreTransform != null)
            {
                TextMeshProUGUI itemsPickupComponent = itemsPickupTransform.GetComponent<TextMeshProUGUI>();
                TextMeshProUGUI totalScoreComponent = totalScoreTransform.GetComponent<TextMeshProUGUI>();

                if (itemsPickupComponent != null && totalScoreComponent != null)
                {
                    itemsPickupComponent.text = "Ripe Collected: " + itemsPickup;
                    totalScoreComponent.text = "Total Score: " + totalScore;
                }
                else
                {
                    Debug.LogError("TextMeshProUGUI component not found on the child.");
                }
            }
            else
            {
                Debug.LogError("Child object not found.");
            }
        }

    }

}
