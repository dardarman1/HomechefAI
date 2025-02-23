using UnityEngine;
using TMPro;

public class Recipe : MonoBehaviour
{
    public TextMeshProUGUI nameText;
    public TextMeshProUGUI urlText;

    private string recipeName;
    private string url;
    private string[] ingredients;
    private string[] instructions;
    
    public void SetRecipeContent() {
        FindAnyObjectByType<RecipeContent>().ShowRecipe(recipeName, url, ingredients, instructions);
    }

    public void SetRecipeEntry(string name, string url, string[] ingredients, string[] instructions) {
        this.ingredients = ingredients;
        this.instructions = instructions;
        recipeName = name;
        this.url = url;

        nameText.text = name;

        var host = new System.Uri(url).Host;
        var domain = host.Substring(host.LastIndexOf('.', host.LastIndexOf('.') - 1) + 1);
            
        urlText.text = domain;
    }
}
