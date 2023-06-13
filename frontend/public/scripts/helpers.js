import axios from "axios";
import alerts from "./alerts.js"

export default {
    async confirmDialog (question, action, popup, user){
      if (action === "reject") {
        var questions = await this.rejectQuestion(question, popup, user)
        return questions
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
        var str = "Are you sure you want to aprove the question " + question._id + "?"
        const ok = await popup.trigger(alerts.confirmDialog(str,user))
        if(ok) {
          (question.flag = "aproved")
          let validated_at = new Date().toLocaleString()
          question["validated_at"] = validated_at
          question["validated_by"] = user
          axios.put(`${process.env.VUE_APP_BACKEND}/importation/imported_questions/` + question._id + `?nome=${user}`, question);
        }
      }
    },

    rejectQuestion: async function (question, popup, user) {
      var str
      var questions = []
      if(question.flag === "rejected"){
        str = "Are you sure you want to remove the question " + question._id + "?"
        const ok = await popup.trigger(alerts.confirmDialog(str,user))
        if(ok){
          await axios.put(`${process.env.VUE_APP_BACKEND}/importation/remove_questions/` + question._id + `?nome=${user}`)
          .then(response => {
            questions = response.data.questions
        }).catch(e => {
          console.log(e)
    })
        return questions
        }
      }
      else{
        str = "Are you sure you want to reject the question " + question._id + "?"
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
      console.log("Edit question: " + question._id);
    },
}
