using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public delegate void OnBarrelStateChange(BarrelController barrel, BarrelStates previous, BarrelStates next);

public abstract class BarrelStates
{
    
    public abstract void Execute(BarrelController barrel, BarrelStateMachine values, float deltaTime);
    public abstract BarrelStates GetNextState(BarrelController barrel, BarrelStateMachine values, float deltaTime);
}

public class Ripe : BarrelStates
{
    public override void Execute(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("RIPE EXECUTE");

        // Change color on barrel
        barrel.GetComponent<SpriteRenderer>().color = Color.green;
    }

    public override BarrelStates GetNextState(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("RIPE GETNEXTSTATE");

        // We don't leave this state
        return this;
    }

    public static Ripe GetInstance()
    {
        Ripe ripe = new Ripe();
        return ripe;
    }
}

public class Ripening : BarrelStates
{
    public override void Execute(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("RIPENING EXECUTE");

        barrel.GetComponent<SpriteRenderer>().color = Color.grey;

        // set v to 0 when visited
        if (values.visited)
        {
            values.v = 0;
        }

        values.t += deltaTime; // continue to rippen
    }

    public override BarrelStates GetNextState(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("RIPENING GETNEXTSTATE");

        if (values.v >= values.vTime)
        {
            values.visited = false;
            return Rotting.GetInstance();
        }

        if (values.t >= values.tTime)
        {
            return Ripe.GetInstance();
        }

        return this;
    }

    public static Ripening GetInstance()
    {
        Ripening ripe = new Ripening();
        return ripe;
    }
}

public class Rotting : BarrelStates
{
    public override void Execute(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("ROTTING EXECUTE");

        barrel.GetComponent<SpriteRenderer>().color = Color.red;

        // set v to 0 when visited
        if (values.visited)
        {
            values.v = 0;
        }

        values.t -= deltaTime; // we are "rotting"
    }

    public override BarrelStates GetNextState(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("ROTTING GETNEXTSTATE");

        if (values.t <= 0)
        {
            return Dead.GetInstance();
        }

        if (values.visited)
        {
            return Ripening.GetInstance();
        }

        return this;
    }

    public static Rotting GetInstance()
    {
        Rotting ripe = new Rotting();
        return ripe;
    }
}

public class Dead : BarrelStates
{
    public override void Execute(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("DEAD EXECUTE");

        // change color of barrel
        barrel.GetComponent<SpriteRenderer>().color = Color.black;
    }

    public override BarrelStates GetNextState(BarrelController barrel, BarrelStateMachine values, float deltaTime)
    {
        Debug.Log("DEAD GETNEXTSTATE");

        // We dont leave this state
        return this;
    }

    public static Dead GetInstance()
    {
        Dead dead = new Dead();
        return dead;
    }
}
