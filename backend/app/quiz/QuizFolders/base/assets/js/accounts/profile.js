(function() {
  $(document).ready(function() {
    enableUploadingAvatar();
    enablePasswordChange();
  });

  function enableUploadingAvatar() {
    $('.change-avatar').dropzone({
      url: InternalAPI.accounts.upload_avatar.urlNoId.replace(/\/$/, ''),
      paramName: 'avatar',
      acceptedFiles: 'image/*',
      previewsContainer: '.avatar-preview',
      thumbnailWidth: 150,
      thumbnailHeight: 150,
      previewTemplate: $('#avatar-preview-template').html(),
      init: function() {
        // Keep only one file in the uploads' queue
        this.on('complete', function(file, message) {
          if (this.files.length > 1) {
              this.removeFile(this.files[0]);
          }
        });
        // Update the total progress bar
        this.on('totaluploadprogress', function(progress) {
          $('.progress .progress-bar').css('width', progress + '%');
        });
        // Show the total progress bar when upload starts
        this.on('sending', function(file) {
          $('.progress').css('opacity', '1');
        });
        // Hide the total progress bar when nothing's uploading anymore
        this.on('queuecomplete', function(progress) {
          $('.progress').css('opacity', '0');
          $('.avatar-preview').css('background-image', 'none');
        });
      }
    });
  }

  function enablePasswordChange() {
    var $modal = $('#change-password-modal');

    $modal.find('input').on('focus', function() {
      $modal.find('.error_msg, .footer-message').remove();
    });
    $modal.find('.send-passwords').click(_ => changePassword($modal));
  }

  function changePassword($container) {
    var $oldPwd    = $container.find('.old-password');
    var $newPwd    = $container.find('.new-password');
    var $newPwdRep = $container.find('.new-password-rep');
    var $message   = $('<p>');

    if ($oldPwd.val() == '' || $newPwd.val() == '' || $newPwdRep.val() == '') {
      $message.addClass('footer-message').text('Preencha todos os campos');
      $container.find('.modal-footer').prepend($message);
    } else if ($newPwd.val() != $newPwdRep.val()) {
      $message.addClass('error_msg').text('Palavras-passe não coincidem');
      $message.insertAfter([$newPwd, $newPwdRep]);
    } else {
      InternalAPI.accounts.change_password({
        'old': $oldPwd.val(),
        'new': $newPwd.val()
      }).done(response => {
        if (response.error) {
          $message.addClass('error_msg').text('Palavra-passe atual errada');
          $message.insertAfter($oldPwd);
        } else {
          $message.addClass('footer-message').text('Palavra-passe alterada com sucesso');
          $container.find('.modal-footer').prepend($message);
        }
      });
    }
  }
})();
