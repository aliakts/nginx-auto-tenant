from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def reload_nginx():
    subprocess.run(["docker", "exec", "nginx", "nginx", "-s", "reload"])

def add_tenant_to_nginx(domain):
    NGINX_CONF_PATH = "/etc/nginx/conf.d/default.conf"
    server_block = f"""
server {{
    listen 80;
    server_name {domain};

    location / {{
        proxy_pass http://sample-app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
    with open(NGINX_CONF_PATH, "a") as conf_file:
        conf_file.write(server_block)

    reload_nginx()

@app.route('/create_tenant', methods=['POST'])
def create_tenant():
    data = request.json
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    try:
        add_tenant_to_nginx(domain)
        return jsonify({"message": f"Tenant for {domain} created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
