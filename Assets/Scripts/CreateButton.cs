using System.Collections.Generic;
using UnityEngine;

public class CreateButton : MonoBehaviour
{
    public Transform ingredientContainer;

    public void Create() {
        List<string> ingredients = new List<string>();

        foreach (Transform child in ingredientContainer) {
            ingredients.Add(child.GetComponentsInChildren<TMPro.TextMeshProUGUI>()[1].text);
        }

        Debug.Log("Ingredients: " + string.Join(", ", ingredients));
    }
}
