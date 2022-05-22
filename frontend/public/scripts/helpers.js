import axios from "axios";
import alerts from "./alerts.js"

export default {
    async confirmDialog (question, action, popup, user){
      if (action === "reject") {
        this.rejectQuestion(question, popup, user)
      } else if (action === "aprove") {
        this.aproveQuestion(question,popup,user)
      }
    },

    aproveQuestion: async function (question, popup, user) {
      if (question.flag === "aproved") {
        popup.display(alerts.errorDialog("Question already approved.",user));
      } else if (question.flag === "rejected") {
        popup.display(alerts.errorDialog("Invalid question.",user));
      }
      else{
        var str = "Are you sure you want to aprove the question " + question.id + "?"
        const ok = await popup.trigger(alerts.confirmDialog(str,user))
        if(ok) {
          (question.flag = "aproved")
          axios.put(`${process.env.VUE_APP_BACKEND}/importation/imported_questions/` + question._id + `?nome=${user}`, question);
        }
      }
    },

    rejectQuestion: async function (question, popup, user) {
      if(question.flag === "rejected"){
        popup.display(alerts.errorDialog("Question already rejected.",user));
      }
      else{
        var str = "Are you sure you want to reject the question " + question.id + "?"
        const ok = await popup.trigger(alerts.confirmDialog(str,user))
        if(ok) {
          (question.flag = "rejected") &&
          axios.put(`${process.env.VUE_APP_BACKEND}/importation/imported_questions/` + question._id + `?nome=${user}`,question);    
        }
      }
    },


    editQuestion: function (question) {
      this.editedIndex = this.questions.indexOf(question);
      this.editedQuestion = Object.assign({}, question);
      this.dialog = true;
      console.log("Edit question: " + question.id);
    },
}
