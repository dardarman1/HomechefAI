using UnityEngine;
using TMPro;

public class RecipeContent : MonoBehaviour
{
    public Animator animator;
    public TextMeshProUGUI nameText;
    public TextMeshProUGUI urlText;
    public TextMeshProUGUI contentText;

    public void ShowRecipe(string name, string url, string[] ingredients, string[] instructions) {
        animator.SetTrigger("Toggle");

        nameText.text = name;
        urlText.text = $"<a href=\"{url}\">{url}</a>";

        GetComponentInChildren<Hyperlink>().url = url;

        string content = "<b>Ingredients:</b>\n";
        foreach (string ingredient in ingredients) {
            content += $"•<indent=5%>{ingredient}</indent>\n";
        }

        content += "\n<b>Instructions:</b>\n";

        int i = 1;
        foreach (string instruction in instructions) {
            content += $"{i++}. {instruction}\n";
        }

        contentText.text = content;
    }
}
