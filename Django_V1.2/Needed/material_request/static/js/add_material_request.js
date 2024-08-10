$(document).ready(function() {
    $('#id_project').change(function() {
        var projectId = $(this).val();
        if (projectId) {
            var url = document.getElementById('some-element').dataset.addMaterialRequestUrl;
            $.ajax({
                url: url,
                data: {
                    'project_id': projectId
                },
                dataType: 'json',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(data) {
                    $('#id_project_code').val(data.code);
                    $('#id_project_location').val(data.location);
                    $('#id_project_consultant').val(data.consultant);
                }
            });
        } else {
            $('#id_project_code').val('');
            $('#id_project_location').val('');
            $('#id_project_consultant').val('');
        }
    });

    $('#product-name').on('input', function() {
        var input = $(this).val();
        if (input.length >= 3) {
            $.ajax({
                url: '/api/products/search',  // Adjust the URL based on your routing
                data: {
                    'name': input
                },
                dataType: 'json',
                success: function(data) {
                    if (data.length > 0) {
                        var product = data[0];
                        $('#product-code').val(product.code);
                        $('#product-unit').val(product.unit);
                        $('#product-description').text(product.description);
                        $('#product-image').attr('src', product.pic_url);  // Ensure you send pic_url from the server
                        $('#product-quantity').attr('max', product.stock);  // Set the max attribute to the stock available
                    }
                }
            });
        }
    });

    // Event handler for updating product quantity
    $('#update-quantity-button').click(function() {
        var productId = $('#product-id').val();  // Assuming you have an input field for product ID
        var newQuantity = $('#product-quantity').val();
        if (parseInt(newQuantity) > parseInt($('#product-quantity').attr('max'))) {
            alert('Requested quantity exceeds available stock!');
            return;
        }
        $.ajax({
            url: '/products/update-quantity/',  // Update with the correct path
            type: 'POST',
            data: {
                product_id: productId,
                quantity: newQuantity
            },
            success: function(response) {
                alert('Quantity updated successfully!');
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);  // Log the server response to the console
                alert('Error updating quantity');
            }
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        var currentDate = new Date().toISOString().slice(0, 16);
        document.getElementById('request-date').value = currentDate;
    });

 
    // Additional code from add_material_request_handlers.js
    $('#id_project').change(function() {
        var projectId = $(this).val();
        if (projectId) {
            $.ajax({
                url: '{% url "add_material_request" %}',
                data: {
                    'project_id': projectId
                },
                dataType: 'json',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(data) {
                    $('#id_project_code').val(data.code);
                    $('#id_project_location').val(data.location);
                    $('#id_project_consultant').val(data.consultant);
                }
            });
        } else {
            $('#id_project_code').val('');
            $('#id_project_location').val('');
            $('#id_project_consultant').val('');
        }
    });

    $('#product-name').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/products/search-products/',  // Adjust the URL based on your actual URL configuration
                dataType: "json",
                data: {
                    name: request.term  // 'q' is the query parameter expected by your Django view
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.name,
                            value: item.name,
                            code: item.code,
                            pic_url: item.pic_url  // Ensure your backend sends this data
                        };
                    }));
                }
            });
        },
        minLength: 2,  // Minimum length of string to trigger the search
        select: function(event, ui) {
            $('#product-code').val(ui.item.code);
            $('#product-image').attr('src', ui.item.pic_url);
            // Reset quantity to 0 each time a new product is selected
            $('#product-quantity').val(0);
        }
    });

    // New event handler for product code input
    $('#product-code').on('input', function() {
        var inputCode = $(this).val();
        if (inputCode.length >= 2) {
            $.ajax({
                url: '/products/search-products/',
                data: { code: inputCode },
                dataType: 'json',
                success: function(data) {
                    if (data.length > 0) {
                        $('#product-name').val(data[0].name);
                    }
                }
            });
        }
    });

    // Handle quantity changes
    $('#product-quantity').change(function() {
        var quantity = $(this).val();
        var productName = $('#product-name').val();
        if (quantity && productName) {
            $.ajax({
                url: '/products/update-quantity/',  // Ensure this URL is correct
                type: 'POST',
                data: {
                    name: productName,
                    quantity: quantity
                },
                success: function(response) {
                    alert('Quantity updated successfully!');
                },
                error: function(xhr, status, error) {
                    alert('Error updating quantity');
                }
            });
        }
    });
});