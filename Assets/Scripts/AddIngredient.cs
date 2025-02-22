using UnityEngine;
using TMPro;

public class AddIngredient : MonoBehaviour
{
    public TMP_InputField ingredientName;
    public GameObject ingredientPrefab;
    public Transform ingredientListParent;

    public void Add() {
        if (ingredientName.text.Trim() == "") {
            return;
        }

        GameObject ingredient = Instantiate(ingredientPrefab, ingredientListParent);
        ingredient.GetComponentsInChildren<TextMeshProUGUI>()[1].text = ingredientName.text;
        Debug.Log("Added ingredient: " + ingredientName.text);
        ingredientName.text = "";
    }
}
