class Products {
    constructor() {
        this.products = []
    }

    getProductByCode(code) {
        return new Promise((resolve, reject) => {
            $.ajax({
                method: 'GET',
                url: 'check_code/',
                data: { code },
                cache: 'false',
                success: (data) => {
                    this.products.push(data.success);
                    resolve();
                },
                error: function(error) {
                    reject({ message: 'Нет на складе'});
                }
            })
        })
    }

    sendProductsReceipt(receipt) {
        if(!this.products.length) {
            return Promise.reject({ message: 'Не выбраны продукты' });
        }
        return new Promise((resolve, reject) => {
            $.ajax({
                method: 'POST',
                url: 'products_receipt/',
                contentType: "application/json",
                dataType: 'json',
                data: JSON.stringify({ products: this.products, paymentType: receipt.paymentType }),
                 headers: {
                   'X-CSRFToken': receipt.token
                 },
                cache: 'false',
                success: (data) => {
                    this.products = [];
                    //В ресолв можно передать data
                    resolve(data.success);
                },
                error: function(error) {
                    reject(error);
                }
            })
        })
    }
}

class ProductTemplate {
    constructor(template, renderTarget, totalTemplate) {
        this.template = template;
        this.renderTarget = renderTarget;
        this.totalTemplate = totalTemplate;
    }

    renderTableBody = (product) => {
        this.template.tmpl(product).appendTo(this.renderTarget);
    }

    renderTotal = (totalData) => {
        this.totalTemplate.tmpl(totalData).appendTo(this.renderTarget);
    }

    cleanTable = () => {
        this.renderTarget.html('')
    }
}

$(document).ready(function () {
    const productsProcessor = new Products();
    const productsTemplate = new ProductTemplate(
        $('#productrow'),
        $("#producttbody"),
        $("#productstotal")
    );

    const form = $('#code-form');
    const codeInput = $('#code');

    const CODE_MIN_CHAR_LENGTH = 8;

    form.on('submit', function(e) {
        e.preventDefault();
        const receiptRequest = {
            token: form.getFormObject().csrfmiddlewaretoken,
            paymentType: form.getFormObject().paymentType
        }

        productsProcessor.sendProductsReceipt(receiptRequest).then((data) => {
            productsTemplate.cleanTable();
            alert(data.message);
        }).catch((error) => {
            alert(error.message);
        });
    })

    codeInput.on('input', function (e) {
        const value = e.currentTarget.value;
        // Если символов будет не CODE_MIN_CHAR_LENGTH то поиграешь с условием и подбереж диапазон
        if(value.length < CODE_MIN_CHAR_LENGTH) {
            return;
        }

        productsProcessor.getProductByCode(value).then(() => {
            productsTemplate.cleanTable();
            const total = productsProcessor.products.reduce((acc, { price }) => {
                acc +=price;
                return acc;
            }, 0)
            productsProcessor.products.map(productsTemplate.renderTableBody);
            productsTemplate.renderTotal({ total });
            codeInput.val('');
        }).catch((error) => {
             alert(error.message);
        });
    })
})