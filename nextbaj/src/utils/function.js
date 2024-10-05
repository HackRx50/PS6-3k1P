async function genAndSaveQuiz(scriptCompiled, name) {
    // Create quiz 
    console.log("\n", "Generating and Saving Quiz");
    
    const prompt = `Generate 10 simple quiz questions with 4 options to choose from, using the content of the script. Keep the questions things that customer should know about Bajaj Allianz. Script: ${scriptCompiled}. It must be in json format with 3 keys: question, options(4) and correctAnswer. Don't answer anything other than the json`;

    const quizAns = await chatCompletion(prompt);

    const cleanedQuizAns = quizAns.replace(/```/g, "").split("json")[1].replace(/\n/g, "");

    const parsedQuizData = JSON.parse(cleanedQuizAns);
    console.log("pp", parsedQuizData);
    
    await uploadQuizData(parsedQuizData, name);
}