import axios from "axios";
import alerts from "./alerts.js"

export default {
    async confirmDialog (question, action, popup){
      if (action === "reject") {
          var str = "Are you sure you want to reject the question " + question.identifier + "?"
          const ok = await popup.trigger(alerts.confirmDialog(str))
          if(ok) this.rejectQuestion(question)
      } else if (action === "aprove") {
          str = "Are you sure you want to aprove the question " + question.identifier + "?"
          const ok = await popup.trigger(alerts.confirmDialog(str))
          if(ok) this.aproveQuestion(question, popup)
      }
    },
    aproveQuestion: function (question, popup) {
      if (question.flag === "aproved") {
          popup.display(alerts.errorDialog("Question already approved."));
      } else if (question.flag === "rejected") {
          popup.display(alerts.errorDialog("Invalid question."));
      } else {
        (question.flag = "aproved") &&
          axios.put(
            "http://localhost:1337/importacao/" + question.id,
            question
          );
      }
    },
    rejectQuestion: function (question) {
        (question.flag = "rejected") &&
        axios.put("http://localhost:1337/importacao/" + question.id, question);
    },
    editQuestion: function (question) {
      this.editedIndex = this.questions.indexOf(question);
      this.editedQuestion = Object.assign({}, question);
      this.dialog = true;
      console.log("Edit question: " + question.id);
    },
}
