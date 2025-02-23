using System.Collections.Generic;
using UnityEngine;

public class CreateButton : MonoBehaviour
{
    public Transform ingredientContainer;
    public Animator recipesContentAnimator;
    public GameObject recipePrefab;
    public Transform recipesContainer;

    public void Create() {
        List<string> ingredients = new List<string>();

        foreach (Transform child in ingredientContainer) {
            ingredients.Add(child.GetComponentsInChildren<TMPro.TextMeshProUGUI>()[1].text);
        }

        if (ingredients.Count == 0) return;

        recipesContentAnimator.SetTrigger("Toggle");
    }
}
