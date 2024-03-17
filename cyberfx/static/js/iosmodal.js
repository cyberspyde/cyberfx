/*!
 * iosmodal.js - a small Bootstrap modal styled like an iOS modal
 * Copyright 2020 Terry Morse
 * MIT license
 */

/**
 * @external $
 * @property {function} modal
 */

const iOSModal = (function () {

  const modalWrapper = document.createElement('div');
  modalWrapper.innerHTML = `
    <div class="modal fade" id="iosmodal" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-dialog-ios" role="document">
        <div class="modal-content">
          <div class="modal-body" id="iosmodal-body">
            <!-- body content goes here -->
          </div>
          <div class="modal-footer">
            <div class="btn-group" id="iosmodal-buttons" role="group">
              <!-- buttons go here -->
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  const modalDiv = modalWrapper.querySelector('.modal.fade');
  const modalDialog = modalDiv.querySelector('.modal-dialog');
  const modalContent = modalDialog.querySelector('.modal-content');
  const modalBody = modalContent.querySelector('.modal-body');
  const modalFooter = modalContent.querySelector('.modal-footer');
  const btnGroup = modalFooter.querySelector('.btn-group');

  /**
   * show the modal
   * @param {Node|string} body - modal body content, DOM Node or string
   * @param {{id,type,class,innerHTML,onclick}[]} buttons - button data
   */
  function show (body, buttons) {

    modalBody.innerHTML = '';
    btnGroup.innerHTML = '';

    if (body) {
      if (typeof body === 'string') {
        modalBody.innerHTML = body;
      } else {
        modalBody.appendChild(body);
      }
    }

    if (buttons) {
      buttons.forEach(btnProps => {
        const btnData = Object.assign({}, btnProps);
        if (btnData.class) {
          btnData.className = btnData.class;
          delete btnData.class;
        }
        const btn = Object.assign(
          document.createElement('button'), btnData);
        // console.log('show btn:', btn);
        btnGroup.appendChild(btn);
      });
    }

    $('#iosmodal').modal('show');
  }

  function hide () {
    $('#iosmodal').modal('hide');
  }

  function customize ({bottom}) {
    if (!bottom) {
      return;
    }
    console.log('iOSModal setting bottom to:', bottom);
    modalDialog.style.bottom = bottom;
  }

  const cssRules = `
    /*!
     * Bootstrap modal styled to look like an iOS modal
     * Copyright 2020 Terry Morse
     * Licensed under MIT
     */
    
    .modal-dialog.modal-dialog-ios {
      position: fixed;
      bottom: 50px; /* match iPhone */
      margin: 0 16px;
      width: calc(100% - 32px);
      display: flex;
      align-items: center;
    }
    
    .modal.fade:not(.show) .modal-dialog.modal-dialog-ios {
      transform: translate(0, 50vh); /* off bottom of screen */
      transition: transform .5s linear;
    }
    
    .modal.fade.show .modal-dialog.modal-dialog-ios {
      transform: translate(0, 0);
      transition: transform .7s ease-out;
    }
    
    /* don't fade in or out */
    #iosmodal.fade.show {
      opacity: 1;
      transition: opacity 1s linear;
    }
    #iosmodal.fade:not(.show) {
      opacity: 1;
      transition: opacity 1s linear;
    }
    
    .modal-dialog.modal-dialog-ios .modal-content {
      border-radius: 12px;
      border: none;
    }
    
    .modal-dialog.modal-dialog-ios .modal-body {
      padding: 1rem 1.5rem;
      text-align: center;
      font-weight: 300;
      font-size: 1rem;
    }
    
    .modal-dialog.modal-dialog-ios .modal-footer {
      justify-content: center;
      padding: 0;
      border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* full-width vertically stacked buttons */
    .modal-dialog.modal-dialog-ios .modal-footer .btn-group {
      width: 100%;
      margin: 0;
      -ms-flex-direction: column;
      flex-direction: column;
      -ms-flex-align: start;
      align-items: flex-start;
      -ms-flex-pack: center;
      justify-content: center;
    }
    
    .modal-dialog.modal-dialog-ios .modal-footer .btn {
      margin: 2px 12px;
      padding: 0.3rem 0.75rem;
      border-style: none;
      border-radius: 8px;
      width: calc(100% - 24px);
    }
    
    .modal-dialog.modal-dialog-ios .modal-footer .btn:hover {
      background-color: rgba(0, 0, 0, 0.15);
    }
    
    /* on wider screens, center modal on screen, and stack buttons
       horizontally
     */
    @media (min-width: 576px) {
    
      .modal-dialog.modal-dialog-ios {
        position: relative;
        top: calc(50vh - 32px);
        margin: 0 auto;
        display: flex;
        align-items: center;
      }
    
      .modal.fade:not(.show) .modal-dialog.modal-dialog-ios {
        transform: none;
      }
    
      .modal-dialog.modal-dialog-ios .modal-footer .btn-group {
        width: 100%;
        margin: 0;
        flex-direction: row;
        align-items: flex-start;
        justify-content: space-evenly;
      }
    
      .modal-dialog.modal-dialog-ios .modal-footer .btn {
      }
    
      #iosmodal.fade.show {
        opacity: 1;
        transition: opacity .4s linear;
      }
      #iosmodal.fade:not(.show) {
        opacity: 0;
        transition: opacity .2s linear;
      }
    
    }
    
    /* iOS modal backdrop is more transparent than default Bootstrap */
    .modal-backdrop.show {
      opacity: 0.1;
    }
  `;

  // add css rules to head
  const style = document.createElement('style');
  style.id = 'iosModalStyle';
  style.textContent = cssRules;
  document.head.appendChild(style);

  // add modal template to body
  document.body.appendChild(modalDiv);

  return {
    customize,
    show,
    hide
  };
})();
