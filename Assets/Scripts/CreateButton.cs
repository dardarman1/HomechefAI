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
        public string name;
        public string url;
        public string[] ingredients;
        public string[] directions;
    }

    public void Create() {
        List<string> ingredients = new List<string>();

        foreach (Transform child in ingredientContainer) {
            ingredients.Add(child.GetComponentsInChildren<TMPro.TextMeshProUGUI>()[1].text);
        }

        if (ingredients.Count == 0) return;

        recipesContentAnimator.SetTrigger("Toggle");


    }

    IEnumerator GetRecipes(List<string> ingredients) {
        string url = "https://my-service-894665829957.us-central1.run.app/get_recipes";
        string ingredientsStr = string.Join(",", ingredients);
        using (UnityWebRequest www = UnityWebRequest.Post(url, $"{{\"ingredients\": [{ingredientsStr}]}}", "application/json"))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.downloadHandler.text);
            }
            else
            {
                string responseText = www.downloadHandler.text;
                Debug.Log(responseText);

                RecipeJSON[] recipes = JsonUtility.FromJson<RecipeJSON[]>(responseText);
                foreach (RecipeJSON recipe in recipes)
                {
                    GameObject recipeObj = Instantiate(recipePrefab, recipesContainer);
                    recipeObj.GetComponent<Recipe>().SetRecipeEntry(recipe.name, recipe.url, recipe.ingredients, recipe.directions);
                }
            }
        }
    }
}
