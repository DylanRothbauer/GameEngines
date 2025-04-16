using Cainos.PixelArtTopDown_Basic;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;

public class BarrelController : MonoBehaviour
{
    
    private BarrelModel model;

    protected OnBarrelStateChange onBarrelStateChange;

    public bool IsCoroutineRunning { get; set; } = false;

    void Start()
    {
        model = GetComponent<BarrelModel>();
        model.currentState = Ripening.GetInstance();
        
    }

    // Update is called once per frame
    void Update()
    {
        if (model != null)
        {
            model.stateValues.v += Time.deltaTime;
            model.currentState.Execute(this, model.stateValues, Time.deltaTime);
            BarrelStates nextState = model.currentState.GetNextState(this, model.stateValues, Time.deltaTime);

            if (onBarrelStateChange != null)
            {
                if (model.currentState == nextState)
                {
                    onBarrelStateChange(this, model.currentState, nextState);

                }
            }

            model.currentState = nextState;
        }
        
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            TopDownCharacterController player = collision.GetComponent<TopDownCharacterController>();
            // mark visited
            model.stateValues.visited = true;

            // pass model to player
            // only collect if it is ripe
            if (this.model.currentState.GetType() == typeof(Ripe))
            {
                Debug.Log("CURRENT STATE IS RIPE AND TRYING TO COLLECT!");

                if (player.onItemPickup != null)
                {
                    // Notify players delegate
                    player.onItemPickup(model);
                } else
                {
                    Debug.LogWarning("ONITEMPICKUP DELEGATE NULL");
                }

                // Remove item?
                //gameObject.SetActive(false);
                //Destroy(gameObject);

                if (FarmablePool.GetInstance() != null)
                {
                    FarmablePool.GetInstance().ReturnBarrel(this);
                } else
                {
                    Debug.Log("FARMABLEPOOL IS NULL");
                }

            }

        }
    }

    private void OnTriggerExit2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            model.stateValues.visited = false;
        }
    }

    public void AddOnBarrelStateChange(OnBarrelStateChange listener)
    {
        onBarrelStateChange += listener;
    }

    public void RemoveOnBarrelStateChange(OnBarrelStateChange listener)
    {
        onBarrelStateChange -= listener;
    }

    public void ResetBarrel()
    {
        model.currentState = Ripening.GetInstance();
        model.stateValues.vTime = 5;
        model.stateValues.tTime = 10;
        model.stateValues.visited = false;
        model.stateValues.v = 0;
        model.stateValues.t = 0;

    }

    public BarrelModel GetModel()
    {
        return model;
    }
}
