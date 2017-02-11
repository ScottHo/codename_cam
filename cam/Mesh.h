#pragma once

#include "System.h"

#include <functional>
#include <vector>

#include "Component.h"
#include "Renderer.h"
#include "Transform.h"

class Shader;

class Mesh : public Component {
public:
	Mesh(Shader &shader,
		 GLuint nvertices,
		 GLfloat **vertices,
		 GLfloat **colours,
		 GLuint type);

	void GetMeshData(Renderer::GetMeshDataEvent event);
protected:
	void RegisterHandlers() override;

private:
	GLuint vao_;
	GLuint type_;
	GLuint count_;

	Shader &shader_;

	std::function<void(Renderer::GetMeshDataEvent)> handler_;

	mat4 ModelMatrix();
};
