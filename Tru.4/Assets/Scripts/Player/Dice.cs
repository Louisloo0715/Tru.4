using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class Dice : MonoBehaviour {

    private Sprite[] diceSides;
    [HideInInspector]
    public bool coroutineAllowed = true;

    public static Dice Instance;
    private void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(this);
    }

    // Use this for initialization
    private void Start () {
       
        diceSides = Resources.LoadAll<Sprite>("DiceSides/");
	}

    
    public void ThrowDice(Image image)
    {
        if (!GameControl.gameOver && coroutineAllowed)
            StartCoroutine(RollTheDice(image));
    }

    private IEnumerator RollTheDice(Image image)
    {
        coroutineAllowed = false;
        int randomDiceSide = 0;
        for (int i = 0; i <= 20; i++)
        {
            randomDiceSide = Random.Range(0, 6);
            image.sprite = diceSides[randomDiceSide];
            yield return new WaitForSeconds(0.05f);
        }

        GameControl.diceSideThrown = randomDiceSide + 1;
        GameControl.Instance.MovePlayer();
    }
}
