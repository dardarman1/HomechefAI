using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class CreateButton : MonoBehaviour
{
    public Transform ingredientContainer;
    public Animator recipesContentAnimator;
    public GameObject recipePrefab;
    public Transform recipesContainer;

    [Serializable]
    public class RecipeJSON
    {
        public string recipe_name;
        public string url;
        public string[] ingredients;
        public string[] directions;
    }

    [Serializable]
    public class IngredientsJSON
    {
        public string[] ingredients;
    }

    public void Create() {
        List<string> ingredients = new List<string>();

        foreach (Transform child in ingredientContainer) {
            ingredients.Add(child.GetComponentsInChildren<TMPro.TextMeshProUGUI>()[1].text);
        }

        if (ingredients.Count == 0) return;

        recipesContentAnimator.SetTrigger("Toggle");

        StartCoroutine(GetRecipes(ingredients));
    }

    IEnumerator GetRecipes(List<string> ingredients) {
        string url = "https://my-service-894665829957.us-central1.run.app/get_recipes";
        IngredientsJSON ingredientsJSON = new IngredientsJSON();
        ingredientsJSON.ingredients = ingredients.ToArray();
        using (UnityWebRequest www = UnityWebRequest.Post(url, JsonUtility.ToJson(ingredientsJSON), "application/json"))
        {   
            www.downloadHandler = new StreamingDownloadHandler(OnChunkReceived, "\n");
            www.timeout = 0; // No timeout

            Debug.Log(System.Text.Encoding.UTF8.GetString(www.uploadHandler.data));
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
                Debug.LogError($"Stream error: {www.error}");
            else
                Debug.Log("Success");
        }
    }

    private void OnChunkReceived(string chunk) {
        Debug.Log("Received chunk: " + chunk);
        RecipeJSON recipe = JsonUtility.FromJson<RecipeJSON>(chunk);

        GameObject recipeEntry = Instantiate(recipePrefab, recipesContainer);
        recipeEntry.GetComponent<Recipe>().SetRecipeEntry(recipe.recipe_name, recipe.url, recipe.ingredients, recipe.directions);
    }
}
